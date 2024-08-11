from typing import List, Dict

import requests
from requests import RequestException

from app.core.rag.data_extractor.factory import DataExtractorFactory
from app.logger import logger
from app.service.task.celery_app import celery_app
from app.utils.url import get_complete_url


@celery_app.task(bind=True)
def process_documents(self, dataset_uuid: str, documents: List[Dict]):
    try:
        logger.info(f"Processing dataset uuid: {dataset_uuid}, document count: {len(documents)}.")

        # Step 1: Load Dataset from document resource url
        for document in documents:
            try:
                # Step 1: Load Resource URL into Memory
                resource_uuid = document.get("resource_uuid")
                resource_url = get_complete_url(document.get("resource_url"))

                logger.info(f"Loading resource UUID: {resource_uuid}, URL: {resource_url}")

                response = requests.get(resource_url)
                if response.status_code != 200:
                    logger.error(
                        f"Failed to load resource from URL: {resource_url} with status code {response.status_code}")
                    continue
            except RequestException as e:
                logger.error(f"Error occurred while processing document: {e}")
                # You can update your task status or take other actions here if needed
                continue  # Continue with the next document

            try:
                # Step 2: Initialize Data Extractor based on Resource Type
                content_type = response.headers.get('Content-Type')
                # print(f"content type: {content_type}")
                if content_type is None:
                    logger.warning(f"Content-Type not found for document UUID: {document.get('resource_uuid')}")
                    continue
                data_extractor = DataExtractorFactory.get_extractor(content_type)

                logger.info(
                    f"Initialized {data_extractor.__class__.__name__} for document UUID: {document.get('resource_uuid')}")

            except ValueError as e:
                logger.error(f"Failed to initialize data extractor for document UUID: {resource_uuid} - {e}")
                continue

            try:
                # Step 3: Initialize Data Extractor based on Resource Type
                data_extractor.parse()
            except ValueError as e:
                logger.error(f"Failed to initialize data extractor for document UUID: {resource_uuid} - {e}")
                continue

    except Exception as e:
        logger.error(f"Unhandled exception in task: {e}")
        # You can update your task status or take other actions here if needed
        # self.retry(exc=e, countdown=60)  # Optionally retry the task after a delay

    return "Task completed"
