import traceback

from app.logger import logger

from app.service.task.celery_app import celery_app
from app.service.task.rag.service import RagProcessorTaskService


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
        logger.error(
            f"Task: {task_id}, document uuid: {service_rag_processor.document.uuid}, Failed to get error: {e}",
            exc_info=True
        )
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
