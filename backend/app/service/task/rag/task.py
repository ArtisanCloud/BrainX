from celery import states

from app import settings
from app.database.session_manager import get_sync_db_session
from app.service.task import logger_rag as logger

from app.service.task.celery_app import celery_app

from app.service.task.rag.service import RagProcessorTaskService


@celery_app.task(bind=True)
def task_process_document(
    self, document_uuid: str, user_uuid: str = None, *args, **kwargs
):
    with get_sync_db_session() as sync_db:

        service_rag_processor = RagProcessorTaskService(
            sync_db, document_uuid, user_uuid, task=self
        )
        task_id = self.request.id
        exception = None
        logger.info(
            f"Start to Task: {task_id}, document UUID: {service_rag_processor.document.uuid}"
        )

        try:
            _, exception = service_rag_processor.process_document()
            if exception is not None:
                raise exception
            sync_db.commit()

        except Exception as e:
            # 发生异常时回滚事务
            logger.error("Exception process_document occurred and rollback the transaction.")
            sync_db.rollback()
            logger.error(
                f"Task: {task_id}, document UUID: {service_rag_processor.document.uuid}, error: {e}",
                exc_info=settings.log.exc_info,
            )
            exception = e

        finally:

            logger.info(
                f"Task: {task_id}, document UUID: {service_rag_processor.document.uuid}, status: completed."
            )
            # 无论任务成功与否，最终更新任务状态
            if exception is not None:
                self.update_state(
                    state=states.FAILURE,
                    meta={
                        "exc_type": str(type(exception)),
                        "exc_message": str(exception),
                    },
                )
                return {"status": "failed", "error": str(exception)}
            else:
                self.update_state(
                    state=states.SUCCESS,
                    meta={
                        "dataset_uuid": service_rag_processor.document.dataset_uuid,
                        "document_uuid": service_rag_processor.document.uuid,
                    },
                )
                return {
                    "status": "success",
                    "document_uuid": service_rag_processor.document.uuid,
                }
