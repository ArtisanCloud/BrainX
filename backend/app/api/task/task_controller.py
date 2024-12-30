import time
from typing import Dict, Any

from celery import states
from fastapi import APIRouter

from app import settings
from app.logger import logger
from app.schemas.task.task import RequestQueryDocumentProcessStatus, RequestRunMultiple30SecondsStatus
from app.service.task.celery_app import celery_app
from celery.result import AsyncResult

from app.service.task.task import TaskService, run_manual_connect_db
from celery import group

router = APIRouter()


@router.post("/30-seconds")
async def run_30_seconds_task():
    if settings.server.environment == 'production':
        return

    task = TaskService.run_30_seconds_task.apply_async()
    return {"task_id": task.id}


@router.post("/run-multiple-30s-tasks")
async def run_multiple_tasks(data: RequestRunMultiple30SecondsStatus):
    if settings.server.environment == 'production':
        return

    # 使用 Celery 的 group 启动多个任务
    task_group = group(TaskService.run_30_seconds_task.s() for _ in range(data.task_count))
    task_group_result = task_group.apply_async()  # 异步执行任务组

    task_ids = [result.id for result in task_group_result]
    # 返回任务 ID 列表
    return {"task_ids": task_ids}  # result.ids 包含所有任务的 ID


@router.post("/run-multiple-30s-tasks-with-locker")
async def run_multiple_tasks_with_locker(data: RequestRunMultiple30SecondsStatus):
    if settings.server.environment == 'production':
        return

    # 使用 Redis 的分布式锁
    # 如果有6个任务，开了2个worker，通过使用分布锁，保证2个worker只有一个worker在执行任务，其他5个任务全部都在队列中等待
    # 就算第二个worker接收到了任务，也需要reject 掉，返回给celery，让任务继续在队列里等待

    # 使用 Celery 的 group 启动多个任务
    task_group = group(TaskService.run_30_seconds_task_with_locker.s() for _ in range(data.task_count))
    task_group_result = task_group.apply_async()  # 异步执行任务组

    task_ids = [result.id for result in task_group_result]
    # 返回任务 ID 列表
    return {"task_ids": task_ids}  # result.ids 包含所有任务的 ID



@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    if settings.server.environment == 'production':
        return

    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == states.STARTED:
        return {
            "state": task_result.state,
            "current": task_result.info.get('current', 0),
            "total": task_result.info.get('total', 1)
        }
    elif task_result.state == states.SUCCESS:
        return {
            "state": task_result.state,
            "result": task_result.result
        }
    else:
        return {"state": task_result.state}


@router.post("/status")
async def get_tasks_status(data: RequestQueryDocumentProcessStatus):
    # 结果字典，用于存储每个 task_id 的状态
    tasks_status: Dict[str, Any] = {}

    for task_id in data.task_uuids:  # 这里获取 task_uuids
        task_result = AsyncResult(task_id, app=celery_app)

        # 根据任务状态添加不同的状态信息
        if task_result.state == states.STARTED:
            tasks_status[task_id] = {
                "state": task_result.state,
                "current": task_result.info.get('current', 0),
                "total": task_result.info.get('total', 1)
            }
        elif task_result.state == states.SUCCESS:
            tasks_status[task_id] = {
                "state": task_result.state,
                "result": task_result.result
            }
        else:
            tasks_status[task_id] = {
                "state": task_result.state
            }

    return tasks_status


@router.post("/run_connect_db")
async def api_run_connect_db():
    # task = TaskService.run_with_connect_db.apply_async()
    task = run_manual_connect_db.apply_async()
    return {"task_id": task.id}


@router.get("/echo_task")
def echo_task():
    
    task = "Task executed"
    
    logger.info(task)

    return {task: task}


@router.get("/run_task")
def run_task():
    task = TaskService.run_task.apply_async()
    return {"task_id": task.id}
