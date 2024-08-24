from io import BytesIO
from typing import Any, List, Tuple

import requests
from fastapi import Depends
from requests import RequestException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rag.indexing.base import IndexingDriverType
from app.core.rag.indexing.extractor.factory import DataExtractorFactory
from app.core.rag.indexing.factory import IndexingFactory
from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.core.rag.indexing.splitter.factory import TextSplitterFactory, SplitterDriverType
from app.dao.rag.document import DocumentDAO
from app.dao.tenant.user import UserDAO
from app.database.deps import get_db_session
from app.logger import logger
from app.models import DocumentSegment, User
from app.models.rag.document import DocumentIndexingStatus, Document, ContentType
from app.models.rag.document_node import DocumentNode


class RagProcessorTaskService:
    def __init__(self,
                 document_uuid: str,
                 user_uuid: str = None,
                 task: Any = None,
                 db: AsyncSession = Depends(get_db_session),
                 ):
        self.task = task
        self.document_dao = DocumentDAO(db)
        self.user_dao = UserDAO(db)
        self.request = None
        self.db = db
        self.document = Document | None
        self.user = User | None

        self.document, exception = self.document_dao.get_by_uuid(document_uuid)
        if exception:
            logger.error(f"get document object error: {exception}")
            raise exception

        if self.document is None:
            msg_error = f"document {document_uuid} cannot be found in db"

            logger.error(msg_error)
            raise Exception(msg_error)

        self.user, exception = self.user_dao.get_by_uuid(user_uuid)
        if exception:
            logger.error(f"get user object error: {exception}")
            raise exception

        if self.document is None:
            msg_error = f"user {document_uuid} cannot be found in db"

            logger.error(msg_error)
            raise Exception(msg_error)

    @staticmethod
    def is_document_available_to_process(document: Document) -> Tuple[bool, Exception | None]:
        """
                检查文档是否可用于处理。

                :return: (是否可处理, 错误或None)
                """
        try:
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

            valid_document_content_types = ContentType.get_content_type_names()  # Adjust as needed
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

    async def process_document(self) -> Exception | None:
        document_segments: List[DocumentSegment] = []
        # print(task_id)

        is_available, exception = self.is_document_available_to_process(self.document)
        if not is_available:
            return exception

            # --------------- Step Load Resource URL into Memory
        try:
            # save document indexing status
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.PARSING)

            # logger.info(f"Loading resource UUID: {resource_uuid}, URL: {resource_url}")
            response = requests.get(self.document.resource_url)
            response.raise_for_status()  # 抛出请求异常

            content_type = response.headers.get('Content-Type')
            if content_type is None:
                raise ValueError(f"Content-Type not found for document UUID: {self.document.uuid}")

            file_data = BytesIO(response.content)
            # logger.info(f"File length: {file_data.getbuffer().nbytes} bytes")

        except RequestException as e:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=e)
            logger.error(f"Task Error occurred while loading resource from URL: {self.document.resource_url} - {e}")
            return e

        # --------------- Step Extract Document text
        try:
            # save document indexing status
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.EXTRACTING)

            data_extractor = DataExtractorFactory.get_extractor(content_type, file_data)
            # logger.info(f"Initialized {extractor.__class__.__name__} for document UUID: {resource_uuid}")

            blocks = data_extractor.extract()

            # convert blocks into a whole text block
            document_content = BaseTextSplitter.merge_blocks_into_text(blocks)

        except ValueError as e:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=e)
            logger.error(f"Task Failed to extract document segments for document UUID: {self.document.uuid} - {e}")
            return e

        # --------------- Step Cleaning nodes
        try:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.SPLITTING)

        except ValueError as e:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=e)
            logger.error(f"Task Failed to cleaning nodes, document uuid: {self.document.uuid} - {e}")
            return e

        # --------------- Step Split into segments
        try:
            # save document indexing status
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.SPLITTING)

            splitter = TextSplitterFactory.get_splitter(SplitterDriverType.LANGCHAIN)
            indexer = IndexingFactory.get_indexer(IndexingDriverType.LANGCHAIN, splitter)
            nodes = indexer.transform_documents([DocumentNode(
                page_content=document_content,
                metadata={
                    "dataset_uuid": self.document.get("dataset_uuid"),
                    "document_uuid": self.document.get("uuid"),
                }
            )])
            # print("transformed nodes:", nodes)

        except ValueError as e:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=e)
            logger.error(
                f"Task Failed to transform the document text to segment, document uuid: {self.document.uuid} - {e}")
            return e

        # --------------- Step 4: Create Document Segments
        try:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.INDEXING)

        except ValueError as e:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.ERROR, error=e)
            logger.error(
                f"Task Failed to index document segments for document UUID, document uuid: {self.document.uuid} - {e}")
            return e

        # --------------- Step 5: Update Document with Indexing Information with status
        try:
            await self.document_dao.set_indexing_status(self.document, DocumentIndexingStatus.INDEXING)
        except ValueError as e:
            logger.error(
                f"Task Failed to update document with indexing information for document UUID: {self.document.uuid} - {e}")
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
            self.db.commit()  # 提交数据库事务
            return True

        except Exception as e:
            print(f"Preprocessing failed: {e}")
            return False
