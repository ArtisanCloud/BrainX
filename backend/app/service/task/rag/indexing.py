from typing import List

from app.logger import logger
from app.models import Document
from app.service.task.celery_app import celery_app


@celery_app.task(bind=True)
def process_dataset(self, documents: List[Document]):
    logger.info(f"process document count: {len(documents)} .")
    print(documents)
    return "Task completed"
