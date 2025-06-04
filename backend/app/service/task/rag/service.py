import urllib.parse
from datetime import datetime
import os
from typing import Any, List, Tuple, Optional

from requests import RequestException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import settings
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.model_manager import ModelManager
from app.core.rag.ingestion.extractor.factory import DataExtractorFactory
from app.core.rag.ingestion.factory import IndexingFactory
from app.core.rag.ingestion.splitter.base import BaseTextSplitter
from app.core.rag.ingestion.splitter.factory import TextSplitterFactory
from app.dao.rag.document import DocumentDAO
from app.dao.rag.document_segment import DocumentSegmentDAO
from app.database.session_manager import is_manual_session
from app.service.task import logger_rag as logger
from app.models import DocumentSegment, User, Dataset
from app.models.base import UTC
from app.models.rag.document import DocumentIndexingStatus, Document, ContentType, DataSourceType
from app.models.rag.document_node import DocumentNode
from app.utils.document import parse_local_document, load_document
from app.utils.url import get_oss_url, get_storage_path


class RagProcessorTaskService:
    def __init__(
            self,
            tenant_uuid: str,
            sync_db: Optional[Session],
            document_uuid: str,
            user_uuid: str,
            task: Any = None,
    ):
        self.tenant_uuid = tenant_uuid
        self.task = task
        self.request = None
        self.document: Document
        self.dataset: Dataset
        self.user: User

        if sync_db is None:
            raise Exception("db session is None")
        self.sync_db = sync_db
        self.model_manager = ModelManager(sync_db=self.sync_db)
        self.document_dao = DocumentDAO(sync_db=self.sync_db)
        self.document_segment_dao = DocumentSegmentDAO(sync_db=self.sync_db)

        # 执行查询逻辑
        self.document = self._get_document(document_uuid)
        self.dataset = self._get_dataset(self.document.dataset_uuid)
        self.user = self._get_user(user_uuid)
        # print(self.document, self.user)

    def _get_document(self, document_uuid: str) -> Document:
        stmt = select(Document).where(Document.uuid == document_uuid)
        document = self.sync_db.execute(stmt).scalars().first()
        if document is None:
            msg_error = f"document uuid: {document_uuid}, error: cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)
        return document

    def _get_dataset(self, dataset_uuid: str) -> Dataset:
        stmt = select(Dataset).where(Dataset.uuid == dataset_uuid)
        dataset = self.sync_db.execute(stmt).scalars().first()
        if dataset is None:
            msg_error = f"dataset uuid: {dataset_uuid}, error: cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)

        return dataset

    def _get_user(self, user_uuid: str) -> User:
        stmt = select(User).where(User.uuid == user_uuid)
        user = self.sync_db.execute(stmt).scalars().first()
        if user is None:
            msg_error = f"user uuid: {user_uuid}, error: cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)
        return user

    def __del__(self):
        # 关闭数据库会话
        if self.sync_db:
            self.sync_db.close()

    @staticmethod
    def is_document_available_to_process(
            document: Document,
    ) -> Tuple[bool, Exception | None]:
        """
        检查文档是否可用于处理。

        :return: (是否可处理, 错误或None)
        """
        try:
            in_process_status = DocumentIndexingStatus.processing_statuses()
            if document.indexing_status in in_process_status:
                msg = f"document uuid: {document.uuid}, message: Document is started and cannot be processed."
                logger.error(msg)
                return False, Exception(msg)

            if document.is_archived:
                msg = f"document uuid: {document.uuid}, message: Document is archived and cannot be processed."
                logger.error(msg)
                return False, Exception(msg)

            if not document.dataset_uuid:
                msg = f"document uuid: {document.uuid}, message: Dataset UUID is missing dataset UUID."
                logger.error(msg)
                return False, Exception(msg)

            if not document.created_user_by:
                msg = f"document uuid: {document.uuid} message: Created user UUID is missing."
                logger.error(msg)
                return False, Exception(msg)

            if document.error_message or document.error_at:
                msg = (
                    f"document uuid: {document.uuid}, Document has an unresolved error."
                )
                logger.error(msg)
                return False, Exception(msg)

            if document.is_paused:
                msg = f"document uuid: {document.uuid}, message: Document is paused and cannot be processed."
                logger.error(msg)
                return False, Exception(msg)

            if not document.resource_uuid and not document.resource_url:
                msg = f"document uuid: {document.uuid}, message: Document is missing resource UUID and URL."
                logger.error(msg)
                return False, Exception(msg)

            valid_document_content_types = ContentType.get_content_type_names()
            if document.content_type not in valid_document_content_types:
                msg = f"document uuid: {document.uuid}, message: Document content type is invalid."
                logger.error(msg)
                return False, Exception(msg)

            if document.process_start_at and document.process_end_at:
                if document.process_start_at > document.process_end_at:
                    msg = f"document uuid: {document.uuid}, message: Document processing times are invalid."
                    logger.error(msg)
                    return False, Exception(msg)

            if not document.dataset_process_rule_uuid:
                msg = f"document uuid: {document.uuid}, message: Batch or dataset process rule UUID is missing."
                logger.info(msg)
                return False, Exception(msg)

            # 如果所有检查都通过
            return True, None

        except Exception as e:
            # 捕获任何意外的错误
            return False, e

    def process_document(self) -> Tuple[List[DocumentSegment] | None, Exception | None]:
        document_segments: List[DocumentSegment] = []
        # print(task_id)

        is_available, exception = self.is_document_available_to_process(self.document)
        if not is_available:
            return None, exception

        # create splitter
        splitter = TextSplitterFactory.get_splitter()

        # create embedding model instance
        embedding_model_instance, exception = self.model_manager.get_model_instance(
            tenant_uuid=self.tenant_uuid,
            provider_id=self.dataset.embedding_model_provider,
            model_type=ModelType.TEXT_EMBEDDING,
            model_id=self.dataset.embedding_model,
        )

        if exception is not None:
            return None, exception

        # create indexer
        indexer = IndexingFactory.get_indexer(
            splitter,
            embedding_model_instance,
            self.user,
            self.document,
        )

        # --------------- Step Load Resource URL into Memory
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid} ~~~~~~~")
        logger.info(
            f"document uuid: {self.document.uuid}, loading resource UUID: {self.document.resource_uuid}, URL: {self.document.resource_url}"
        )
        try:
            file_data = None
            # save document ingestion status
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.PARSING
            )

            # logger.info(f"Loading resource UUID: {resource_uuid}, URL: {resource_url}")
            # complete_url, is_url = get_storage_complete_url(self.document.resource_url)
            if (
                    self.document.data_source_type == DataSourceType.OSS_URL.value
                    or self.document.data_source_type == DataSourceType.CRAWLER_URL.value
                    or self.document.data_source_type == DataSourceType.IMPORT_PLATFORM.value
            ):
                complete_url = self.document.resource_url
                # 需要拼接oss url resource
                if self.document.data_source_type == DataSourceType.OSS_URL.value:
                    complete_url = get_oss_url(self.document.resource_url)
                logger.info(
                    f"document uuid: {self.document.uuid}, complete_url: {complete_url} "
                )
                doc, err = load_document(complete_url)
                if err is not None:
                    raise Exception(f"parse http document error: {err}")

                content_type = doc.get("mime_type")
                if content_type is None:
                    raise Exception(
                        f"Content-Type not found for document UUID: {str(self.document.uuid)}"
                    )
                file_data = doc.get("content")
            else:
                complete_url = get_storage_path(self.document.resource_url)
                logger.info(
                    f"document uuid: {self.document.uuid}, complete_path: {complete_url} "
                )
                if os.path.exists(complete_url):
                    doc, exception = parse_local_document(
                        urllib.parse.urlparse(self.document.resource_url),
                        complete_url,
                    )
                    if exception is not None:
                        raise Exception(f"parse local document error: {exception}")
                    content_type = doc.get("mime_type")
                    file_data = doc.get("content")

                else:
                    raise Exception(f"File not found: {complete_url}")

            # logger.info(f"File length: {file_data.getbuffer().nbytes} bytes")

        except RequestException as e:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.ERROR, error=str(e)
            )
            logger.error(
                f"document uuid: {self.document.uuid}, Task Error occurred while loading resource from URL: {self.document.resource_url} - {e}"
            )
            return None, e

        # --------------- Step Extract Document text
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid} ~~~~~~~")
        logger.info(
            f"document uuid: {self.document.uuid}, Step Extract Document text, extractor_type: '{content_type}'")
        try:
            # save document ingestion status
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.EXTRACTING
            )

            data_extractor = DataExtractorFactory.get_extractor(content_type, file_data)
            # logger.info(f"Initialized {extractor.__class__.__name__} for document UUID: {resource_uuid}")

            blocks = data_extractor.extract()

            # convert blocks into a whole text block
            document_content = BaseTextSplitter.merge_blocks_into_text(blocks)
            # print("document content:",document_content)
            if document_content is None or document_content == "":
                raise Exception("parsed document content is empty")

        except Exception as e:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.ERROR, error=str(e)
            )
            logger.error(
                f"document uuid: {self.document.uuid}, Task Failed to extract document segments: {e}"
            )
            return None, e

        # --------------- Step Cleaning nodes and Split into nodes
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid} ~~~~~~~")
        logger.info(
            f"document uuid: {self.document.uuid}, Step Cleaning nodes and Split into nodes"
        )
        try:
            # save document ingestion status
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.SPLITTING
            )
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.CLEANING
            )

            nodes = indexer.transform_documents(
                [
                    DocumentNode(
                        page_content=document_content,
                        metadata={
                            "dataset_uuid": str(self.document.dataset_uuid),
                            "document_uuid": str(self.document.uuid),
                        },
                    )
                ]
            )
            # print("transformed nodes:", nodes)

        except Exception as e:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.ERROR, error=str(e)
            )
            logger.error(
                f"document uuid: {self.document.uuid}, Task Failed to transform the document text to segment - {e}"
            )
            return None, e

        # --------------- Step 4: Create Document Segments
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid} ~~~~~~~")
        logger.info(
            f"document uuid: {self.document.uuid}, Create Document Segments, split nodes length: {len(nodes)}"
        )
        try:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.INDEXING
            )

            document_segments = indexer.create_document_segments(nodes)
            # print(document_segments)
            document_segments, exception = self.document_segment_dao.sync_create_many(
                document_segments
            )
            if exception is not None:
                raise exception

        except Exception as e:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.ERROR, error=str(e)
            )
            logger.error(
                f"document uuid: {str(self.document.uuid)}, Task Failed to index document segments - {e}"
            )
            return None, e

        # --------------- Step 5: Update Document with Indexing Information with status
        logger.info(
            f"~~~~~~~ Process document UUID: {self.document.uuid}, Update Document with Indexing Information with status ~~~~~~~")
        try:
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.STORING
            )
            # get embedding model_provider from current user setup
            word_count, token, exception = indexer.save_nodes_to_store_vector(nodes)

            if exception is not None:
                raise exception

            # save dataset and document status completion
            self.document_dao.set_indexing_status(
                self.document, DocumentIndexingStatus.COMPLETED
            )

            # save word count and used token
            self.document_dao.set_word_count(self.document, word_count)

        except Exception as e:
            logger.error(
                f"document uuid: {str(self.document.uuid)}, Task Failed to update document with indexing information - {e}"
            )
            return None, e

        return document_segments, None

    def preprocess_document(self, document: Document) -> bool:
        """
        预处理文档，尝试解决错误和解除暂停状态。

        :param document: 要预处理的文档实例
        :return: 是否成功进行预处理（例如解除暂停或修复错误）
        """
        try:
            # 如果文档有错误，尝试处理错误
            if document.error_message and document.error_at:
                # 这里可以加入你的错误处理逻辑，尝试自动修复
                # 假设处理成功，清空错误信息
                document.error_message = None
                document.error_at = None
                logger.error("Error has been resolved.")

            # 如果文档处于暂停状态，解除暂停
            if document.is_paused:
                document.is_paused = False
                document.paused_by = None
                document.paused_at = None
                logger.error("Document has been unpaused.")

            # 保存预处理后的状态
            return True

        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return False

    def reset_document(self) -> Optional[Exception]:
        try:
            self.document.updated_user_by = None  # 重置更新用户
            self.document.indexing_status = (
                DocumentIndexingStatus.PENDING
            )  # 设置初始索引状态，假设有一个枚举类型
            self.document.process_start_at = None  # 重置处理开始时间
            self.document.process_end_at = None  # 重置处理结束时间
            self.document.word_count = 0  # 重置字数为0
            self.document.parse_start_at = None  # 重置解析开始时间
            self.document.clean_start_at = None  # 重置清理开始时间
            self.document.split_start_at = None  # 重置分割开始时间
            self.document.token_count = 0  # 重置token计数为0
            self.document.indexing_latency = 0.0  # 重置索引延迟为0.0
            self.document.is_paused = False  # 重置暂停状态为False
            self.document.paused_by = None  # 重置暂停的用户
            self.document.paused_at = None  # 重置暂停时间
            self.document.error_message = None  # 重置错误信息
            self.document.error_at = None  # 重置错误时间
            self.document.is_archived = False  # 重置归档状态为False
            self.document.archived_reason = None  # 重置归档原因
            self.document.archived_by = None  # 重置归档的用户
            self.document.archived_at = None  # 重置归档时间
            self.document.updated_at = datetime.now(UTC)  # 更新操作时间为当前时间

            # 保存预处理后的状态
            if not is_manual_session(self.sync_db):
                self.sync_db.commit()  # 提交数据库事务
            return None

        except Exception as e:
            logger.error(f"Reset failed: {e}")
            self.sync_db.rollback()  # 回滚数据库事务
            return e

        # finally:
        #     self.sync_db.close()
