import time
from typing import Any

from app.logger import logger
from app.service.task.celery_app import celery_app


class TaskService:

    def __init__(self, task: Any):
        # 初始化任务服务
        self.task = task
        pass

    @celery_app.task(bind=True)
    def run_30_seconds_task(self, *args, **kwargs):
        # 使用类实例调用任务
        # print("task _30_seconds_task:", self, args, kwargs)
        instance = TaskService(self)
        return instance._run_30_seconds_task()

    def _run_30_seconds_task(self) -> str:
        # print("run _30_seconds_task", self, self.task)
        for i in range(30):
            time.sleep(1)
            logger.info(f"Seconds elapsed: {i + 1}")
            self.task.update_state(state='PROGRESS', meta={'current': i + 1, 'total': 30})
        return "Task completed"
