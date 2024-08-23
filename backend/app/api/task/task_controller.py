from fastapi import APIRouter

from app import settings
from app.api.rag.document_controller import rag_queue
from app.service.task.celery_app import celery_app
from celery.result import AsyncResult

from app.service.task.task import TaskService

router = APIRouter()


@router.post("/30-seconds")
async def run_30_seconds_task():
    if settings.server.environment == 'production':
        return

    task = TaskService.run_30_seconds_task.apply_async()
    return {"task_id": task.id}


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    if settings.server.environment == 'production':
        return

    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PROGRESS':
        return {
            "state": task_result.state,
            "current": task_result.info.get('current', 0),
            "total": task_result.info.get('total', 1)
        }
    elif task_result.state == 'SUCCESS':
        return {
            "state": task_result.state,
            "result": task_result.result
        }
    else:
        return {"state": task_result.state}
