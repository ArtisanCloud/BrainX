# 初始化 APScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.api.task.task_controller import  run_task
from app.logger import logger


class Scheduler:
    def __init__(self):
        # self.scheduler = BackgroundScheduler()
        self.scheduler = AsyncIOScheduler()

    def start(self):
        logger.info("Starting APScheduler...")
        self.scheduler.start()
        logger.info("APScheduler started.")

    def shutdown(self):
        logger.info("Shutting down APScheduler...")
        self.scheduler.shutdown()
        logger.info("APScheduler shut down.")

    def init_scheduler(self):
        # 启动测试任务执行
        # self.scheduler.add_job(echo_task, IntervalTrigger(seconds=10))
        # self.scheduler.add_job(TaskService.run_30_seconds_task, IntervalTrigger(seconds=10))
        # self.scheduler.add_job(run_task, IntervalTrigger(seconds=10))

        # 添加和配置项目任务
        pass

