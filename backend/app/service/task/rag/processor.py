import traceback
from io import BytesIO
from typing import List, Dict, Any

import requests
from fastapi import Depends
from requests import RequestException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rag.indexing.extractor.factory import DataExtractorFactory
from app.core.rag.indexing.base import IndexingDriverType
from app.core.rag.indexing.factory import IndexingFactory

from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.core.rag.indexing.splitter.factory import TextSplitterFactory, SplitterDriverType
from app.dao.rag.document import DocumentDAO
from app.dao.tenant.user import UserDAO
from app.database.deps import get_db_session
from app.logger import logger
from app.models import DocumentSegment, User
from app.models.rag.document import DocumentIndexingStatus
from app.models.rag.document_node import DocumentNode
from app.service.task.celery_app import celery_app


@celery_app.task(bind=True)
def task_process_document(self, document_uuid: str, user_uuid: str = None, *args, **kwargs):
    service_rag_processor = RagProcessorTaskService(self, document_uuid, user_uuid)
    task_id = self.request.id
    exception = None

    try:
        exception = service_rag_processor.process_document()
        if exception is not None:
            raise exception

    except Exception as e:
        track_lines = traceback.format_exc()
        logger.error(
            f"Task: {task_id}, document uuid: {service_rag_processor.document.uuid}, Failed to get error: {e}\nTraceback: {track_lines}")
        exception = e

    finally:

        logger.info(f"Task: {task_id} for document UUID: {self.document.get('uuid')} completed.")
        # 无论任务成功与否，最终更新任务状态
        if exception is not None:
            self.update_state(state='FAILURE',
                              meta={'exc_type': str(type(exception)), 'exc_message': str(exception)})
            return {"status": "failed", "error": str(exception)}
        else:
            self.update_state(state='SUCCESS',
                              meta={'dataset_uuid': self.document.dataset_uuid,
                                    'document_uuid': self.document.uuid})
            return {"status": "success", "document_uuid": self.document.uuid}


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

    async def process_document(self) -> Exception | None:
        document_segments: List[DocumentSegment] = []
        # print(task_id)

        # 总的 try 块，包含所有步骤
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
