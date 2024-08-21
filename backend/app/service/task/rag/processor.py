import traceback
from io import BytesIO
from typing import List, Dict

import requests
from requests import RequestException

from app.core.rag.extractor.factory import DataExtractorFactory
from app.core.rag.indexing.base import IndexingDriverType
from app.core.rag.indexing.factory import IndexingFactory

from app.core.rag.splitter.base import BaseTextSplitter
from app.core.rag.splitter.factory import TextSplitterFactory, SplitterDriverType
from app.logger import logger
from app.models import DocumentSegment
from app.models.rag.document_node import DocumentNode
from app.service.task.celery_app import celery_app
from app.utils.url import get_complete_url


@celery_app.task(bind=True)
def task_process_document(self, dataset_uuid: str, document: Dict):
    task_id = self.request.id
    resource_uuid = document.get("resource_uuid")
    exception = None
    try:
        exception = process_document(task_id, dataset_uuid, document)
        if exception is not None:
            raise exception

    except Exception as e:
        track_lines = traceback.format_exc()
        logger.error(f"Task Failed to get error: {resource_uuid} - {e}\nTraceback: {track_lines}")
        exception = e

    finally:

        logger.info(f"Task for document UUID: {document.get('uuid')} completed.")
        # 无论任务成功与否，最终更新任务状态
        if exception is not None:
            self.update_state(state='FAILURE', meta={'exc_type': str(type(exception)), 'exc_message': str(exception)})
            return {"status": "failed", "error": str(exception)}
        else:
            self.update_state(state='SUCCESS',
                              meta={'dataset_uuid': dataset_uuid, 'document_uuid': document.get('uuid')})
            return {"status": "success", "document_uuid": document.get('uuid')}


def process_document(task_id: str, dataset_uuid: str, document: Dict) -> Exception | None:
    document_segments: List[DocumentSegment] = []
    resource_uuid = document.get("resource_uuid")
    resource_url = get_complete_url(document.get("resource_url"))
    # print(task_id)

    # 总的 try 块，包含所有步骤
    logger.info(
        f"Processing taskid: {task_id}, dataset uuid: {dataset_uuid}, document uuid: {document.get('uuid')}.")

    # --------------- Step 1: Load Resource URL into Memory
    try:
        # logger.info(f"Loading resource UUID: {resource_uuid}, URL: {resource_url}")
        response = requests.get(resource_url)
        response.raise_for_status()  # 抛出请求异常

    except RequestException as e:
        logger.error(f"Task Error occurred while loading resource from URL: {resource_url} - {e}")
        return e

    # --------------- Step 2: Extract Document text and split into segments
    try:
        content_type = response.headers.get('Content-Type')
        if content_type is None:
            raise ValueError(f"Content-Type not found for document UUID: {resource_uuid}")

        file_data = BytesIO(response.content)
        # logger.info(f"File length: {file_data.getbuffer().nbytes} bytes")

        data_extractor = DataExtractorFactory.get_extractor(content_type, file_data)
        # logger.info(f"Initialized {extractor.__class__.__name__} for document UUID: {resource_uuid}")

        blocks = data_extractor.extract()

        document_content = BaseTextSplitter.merge_blocks_into_text(blocks)

    except ValueError as e:
        logger.error(f"Task Failed to extract document segments for document UUID: {resource_uuid} - {e}")
        return e

    # --------------- Step 3: Transform the text into segments
    try:
        splitter = TextSplitterFactory.get_splitter(SplitterDriverType.LANGCHAIN)
        indexer = IndexingFactory.get_indexer(IndexingDriverType.LANGCHAIN, splitter)
        nodes = indexer.transform_documents([DocumentNode(
            page_content=document_content,
            metadata={
                "dataset_uuid": document.get("dataset_uuid"),
                "document_uuid": document.get("uuid"),
            }
        )])
        # print("transformed nodes:", nodes)

    except ValueError as e:
        logger.error(f"Task Failed to transform the document text to segment: {resource_uuid} - {e}")
        return e
    # --------------- Step 4: Create Document Segments
    try:
        pass
        # indexer = IndexingFactory.get_indexer(IndexingDriverType.LANGCHAIN)
        # exception = indexer.vectorize_segments(document_segments)
        # if exception is not None:
        #     return exception

    except ValueError as e:
        logger.error(f"Task Failed to index document segments for document UUID: {resource_uuid} - {e}")
        return e

    # --------------- Step 5: Update Document with Indexing Information with status
    try:
        document_index = 1
    except ValueError as e:
        logger.error(
            f"Task Failed to update document with indexing information for document UUID: {resource_uuid} - {e}")
        return e

    return None
