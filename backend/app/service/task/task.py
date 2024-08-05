import time

from app.logger import logger
from app.service.task.celery_app import celery_app


@celery_app.task(bind=True)
def _30_seconds_task(self):
    for i in range(30):
        time.sleep(1)
        logger.info(f"Seconds elapsed: {i + 1}")
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': 30})
    return "Task completed"
