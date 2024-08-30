from datetime import datetime
from io import BytesIO
from typing import Any, List, Tuple, Optional

import requests
from requests import RequestException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import settings
from app.core.ai_model.model_manager import ModelManager
from app.core.rag import FrameworkDriverType
from app.core.rag.indexing.extractor.factory import DataExtractorFactory
from app.core.rag.indexing.factory import IndexingFactory
from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.core.rag.indexing.splitter.factory import TextSplitterFactory
from app.dao.rag.document import DocumentDAO
from app.dao.rag.document_segment import DocumentSegmentDAO
from app.logger import logger
from app.models import DocumentSegment, User, Dataset
from app.models.base import UTC
from app.models.model_provider.provider_model import ModelType
from app.models.rag.document import DocumentIndexingStatus, Document, ContentType
from app.models.rag.document_node import DocumentNode
from app.utils.url import get_storage_complete_url


class RagProcessorTaskService:
    def __init__(self,
                 db: Optional[Session],
                 document_uuid: str, user_uuid: str,
                 task: Any = None
                 ):
        self.task = task
        self.request = None
        self.document: Document
        self.dataset: Dataset
        self.user: User

        if db is None:
            raise Exception("db session is None")
        self.db = db
        self.model_manager = ModelManager(FrameworkDriverType(settings.agent.framework_driver))
        self.document_dao = DocumentDAO(self.db)
        self.document_segment_dao = DocumentSegmentDAO(self.db)

        # 执行查询逻辑
        self.document = self._get_document(document_uuid)
        self.dataset = self._get_dataset(self.document.dataset_uuid)
        self.user = self._get_user(user_uuid)
        # print(self.document, self.user)

    def _get_document(self, document_uuid: str) -> Document:
        stmt = select(Document).where(Document.uuid == document_uuid)
        document = self.db.execute(stmt).scalars().first()
        if document is None:
            msg_error = f"document {document_uuid} cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)
        return document

    def _get_dataset(self, dataset_uuid: str) -> Dataset:
        stmt = select(Dataset).where(Dataset.uuid == dataset_uuid)
        dataset = self.db.execute(stmt).scalars().first()
        if dataset is None:
            msg_error = f"dataset {dataset_uuid} cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)

        return dataset

    def _get_user(self, user_uuid: str) -> User:
        stmt = select(User).where(User.uuid == user_uuid)
        user = self.db.execute(stmt).scalars().first()
        if user is None:
            msg_error = f"user {user_uuid} cannot be found in db"
            logger.error(msg_error)
            raise Exception(msg_error)
        return user

    def __del__(self):
        # 关闭数据库会话
        if self.db:
            self.db.close()

    @staticmethod
    def is_document_available_to_process(document: Document) -> Tuple[bool, Exception | None]:

        """
                检查文档是否可用于处理。

                :return: (是否可处理, 错误或None)
                """
        try:
            in_process_status = DocumentIndexingStatus.processing_statuses()
            if document.status in in_process_status:
                logger.info(f"Document {document.uuid} is started.")
                return False, Exception("Document is started and cannot be processed.")

            if document.is_archived:
                logger.info(f"Document {document.uuid} is archived.")
                return False, Exception("Document is archived and cannot be processed.")

            if not document.dataset_uuid:
                logger.info(f"Document {document.uuid} is missing dataset UUID.")
                return False, Exception("Dataset UUID is missing.")

            if not document.created_user_by:
                logger.info(f"Document {document.uuid} is missing created user UUID.")
                return False, Exception("Created user UUID is missing.")

            if document.error_message or document.error_at:
                logger.info(f"Document {document.uuid} has unresolved errors.")
                return False, Exception("Document has an unresolved error.")

            if document.is_paused:
                logger.info(f"Document {document.uuid} is paused.")
                return False, Exception("Document is paused and cannot be processed.")

            if not document.resource_uuid and not document.resource_url:
                logger.info(f"Document {document.uuid} is missing both resource UUID and URL.")
                return False, Exception("Both resource UUID and URL are missing.")

            valid_document_content_types = ContentType.get_content_type_names()
            if document.content_type not in valid_document_content_types:
                logger.info(f"Document {document.uuid} has an invalid document content type.")
                return False, Exception("Document content type is not valid for processing.")

            if document.process_start_at and document.process_end_at:
                if document.process_start_at > document.process_end_at:
                    logger.info(f"Document {document.uuid} has invalid processing times.")
                    return False, Exception("Process start time cannot be after process end time.")

            if not document.dataset_process_rule_uuid:
                logger.info(f"Document {document.uuid} is missing dataset process rule UUID.")
                return False, Exception("Batch or dataset process rule UUID is missing.")

            # 如果所有检查都通过
            return True, None

        except Exception as e:
            # 捕获任何意外的错误
            return False, e

    def process_document(self) -> Exception | None:
        document_segments: List[DocumentSegment] = []
        # print(task_id)

        is_available, exception = self.is_document_available_to_process(self.document)
        if not is_available:
            return exception

        # create splitter
        splitter = TextSplitterFactory.get_splitter(FrameworkDriverType.LANGCHAIN)

        # create embedding model instance
        embedding_model_instance, exception = self.model_manager.get_model_instance(
            self.db, self.document.tenant_uuid,
            self.dataset.embedding_model_provider,
            ModelType.TEXT_EMBEDDING
        )

        if exception is not None:
            return exception

        # create indexer
        indexer = IndexingFactory.get_indexer(
            FrameworkDriverType(settings.agent.framework_driver),
            splitter, embedding_model_instance,
            self.user, self.document,
        )

        # --------------- Step Load Resource URL into Memory
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid}, "
                    f"loading resource UUID: {self.document.resource_uuid}, URL: {self.document.resource_url}")
        try:
            # save document indexing status
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.PARSING)

            # logger.info(f"Loading resource UUID: {resource_uuid}, URL: {resource_url}")
            response = requests.get(get_storage_complete_url(self.document.resource_url))
            response.raise_for_status()  # 抛出请求异常

            content_type = response.headers.get('Content-Type')
            if content_type is None:
                raise Exception(f"Content-Type not found for document UUID: {str(self.document.uuid)}")

            file_data = BytesIO(response.content)
            # logger.info(f"File length: {file_data.getbuffer().nbytes} bytes")

        except RequestException as e:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=str(e))
            logger.error(f"Task Error occurred while loading resource from URL: {self.document.resource_url} - {e}")
            return e

        # --------------- Step Extract Document text
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid}, "
                    f"Step Extract Document text")
        try:
            # save document indexing status
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.EXTRACTING)

            data_extractor = DataExtractorFactory.get_extractor(content_type, file_data)
            # logger.info(f"Initialized {extractor.__class__.__name__} for document UUID: {resource_uuid}")

            blocks = data_extractor.extract()

            # convert blocks into a whole text block
            document_content = BaseTextSplitter.merge_blocks_into_text(blocks)

        except Exception as e:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=str(e))
            logger.error(f"Task Failed to extract document segments for document UUID: {str(self.document.uuid)} - {e}")
            return e

        # --------------- Step Cleaning nodes and Split into nodes
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid}, "
                    f"Step Cleaning nodes and Split into nodes")
        try:
            # save document indexing status
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.SPLITTING)
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.CLEANING)

            nodes = indexer.transform_documents([DocumentNode(
                page_content=document_content,
                metadata={
                    "dataset_uuid": str(self.document.dataset_uuid),
                    "document_uuid": str(self.document.uuid),
                }
            )])
            # print("transformed nodes:", nodes)

        except Exception as e:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=str(e))
            logger.error(
                f"Task Failed to transform the document text to segment, document uuid: {str(self.document.uuid)} - {e}")
            return e

        # --------------- Step 4: Create Document Segments
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid}, "
                    f"Create Document Segments, split nodes length: {len(nodes)}")
        try:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.INDEXING)

            document_segments = indexer.create_document_segments(nodes)
            # print(document_segments)
            document_segments, exception = self.document_segment_dao.sync_create_many(document_segments)
            if exception is not None:
                raise exception

        except Exception as e:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=str(e))
            logger.error(
                f"Task Failed to index document segments for document UUID, document uuid: {str(self.document.uuid)} - {e}")
            return e

        # --------------- Step 5: Update Document with Indexing Information with status
        logger.info(f"~~~~~~~ Process document UUID: {self.document.uuid}, Update Document with Indexing Information with status")
        try:
            self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.INDEXING)
            # get embedding model_provider from current user setup
            exception = indexer.save_nodes_to_store_vector(nodes)

            if exception is not None:
                raise exception

        except Exception as e:
            logger.error(
                f"Task Failed to update document with indexing information for document UUID: {str(self.document.uuid)} - {e}")
            return e

        return None

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
                print("Error has been resolved.")

            # 如果文档处于暂停状态，解除暂停
            if document.is_paused:
                document.is_paused = False
                document.paused_by = None
                document.paused_at = None
                print("Document has been unpaused.")

            # 保存预处理后的状态
            return True

        except Exception as e:
            print(f"Preprocessing failed: {e}")
            return False

    def reset_document(self) -> Optional[Exception]:
        try:
            self.document.updated_user_by = None  # 重置更新用户
            self.document.indexing_status = DocumentIndexingStatus.PENDING  # 设置初始索引状态，假设有一个枚举类型
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
            # self.db.commit()  # 提交数据库事务
            return None

        except Exception as e:
            print(f"Reset failed: {e}")
            return e

        # finally:
        #     self.db.close()
