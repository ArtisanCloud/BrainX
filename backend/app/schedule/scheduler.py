# 初始化 APScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.interval import IntervalTrigger

from app.api.task.task_controller import echo_task
from app.config.config import settings
from app.logger import logger
from app.service.task.task import TaskService


class Scheduler:
    def __init__(self):
        # self.scheduler = BackgroundScheduler()

        # 加载 job_stores 配置
        if settings.schedule.job_stores["default"].type == "redis":

            redis_config = {
                "host": settings.schedule.job_stores["default"].host,
                "port": settings.schedule.job_stores["default"].port,
                "db": settings.schedule.job_stores["default"].db,
                "password": settings.schedule.job_stores["default"].password,  # 可选
                "username": settings.schedule.job_stores["default"].username,  # 可选
            }
            job_stores = {
                "default": RedisJobStore(**redis_config)  # 传递连接参数给 RedisJobStore
            }
        elif settings.schedule.job_stores["default"].type == "sqlalchemy":
            job_stores = {
                "default": SQLAlchemyJobStore(
                    url=settings.schedule.job_stores["default"].url
                )
            }
        else:
            raise ValueError("Invalid job store type")

        # 加载 executors 配置
        executors = {
            "default": ThreadPoolExecutor(
                max_workers=settings.schedule.executors["default"].max_workers
            )
        }

        # 加载 job_defaults 配置
        job_defaults = settings.schedule.job_defaults.model_dump()

        self.scheduler = AsyncIOScheduler(
            jobstores=job_stores,
            executors=executors,
            job_defaults=job_defaults,
        )

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
        self.start_job(
            job_id = "echo_task_job",
            task_func = echo_task,
            interval_seconds=10
        )
        # self.scheduler.add_job(lambda: TaskService.run_30_seconds_task.delay())
        # self.scheduler.add_job(run_task, IntervalTrigger(seconds=10))

        # 添加和配置项目任务
        # self.start_job(self.check_and_run_task, IntervalTrigger(seconds=30), id='run_30_seconds_task', replace_existing=True)

        return
    
    def start_job(self, job_id, task_func, interval_seconds=10,replace_existing=True):
        self.scheduler.add_job(task_func, IntervalTrigger(seconds=interval_seconds), id=job_id, replace_existing=replace_existing)
        logger.info(f"Job {job_id} started.")

    def stop_job(self, job_id):
        job = self.scheduler.get_job(job_id)
        if job:
            job.remove()
            logger.info(f"Job {job_id} stopped.")

    