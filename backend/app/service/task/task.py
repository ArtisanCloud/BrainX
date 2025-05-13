import time

from celery import Task, states
from sqlalchemy import text

from app.database.session_manager import get_sync_db_session

from app import settings
from app.database.session import sync_session_local
from app.service.task import logger
from app.models import User
from app.service.task.celery_app import celery_app
from app.cache.factory import CacheFactory

TASK_30S_SYNC_LOCK_KEY = "lock:task_multiple_30s_tasks_sync"


@celery_app.task
def run_manual_connect_db():
    # 手动启动生成器
    sync_db = sync_session_local()
    sync_db.execute(text(f"SET search_path TO {settings.database.db_schema}, public"))

    try:
        # 获取数据库会话对象
        # 使用 db 进行数据库操作
        result = sync_db.query(User).limit(1).scalar()
        print("manual operation:", result)
        sync_db.commit()
    except Exception as e:
        # 处理异常
        sync_db.rollback()
        raise e

    finally:
        sync_db.close()
        # 手动关闭生成器
        logger.info("finally finished")

    return "connect db"


class TaskService:

    def __init__(self, task: Task):
        # 初始化任务服务
        self.task = task
        pass

    @celery_app.task(bind=True)
    def run_task(self, *args, **kwargs):
        logger.info(f"run task done")

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
            logger.info(f"Task {self.task.request.id} Seconds elapsed: {i + 1}")
            self.task.update_state(
                state=states.STARTED, meta={"current": i + 1, "total": 30}
            )
        return "Task completed"

    @celery_app.task(bind=True)
    def run_30_seconds_task_with_locker(self, *args, **kwargs):
        task: Task = self
        """任务入口，带有分布式锁"""
        cache = CacheFactory.get_cache()

        # 先尝试获取锁，设置锁的超时时间，防止死锁
        timeout = 30 * 60  # 锁的超时时间，设置为30分钟
        lock_acquired = cache.acquire_lock(
            TASK_30S_SYNC_LOCK_KEY, timeout=timeout
        )  # 自动过期时间
        logger.info(f"Task {task.request.id} has locked: {lock_acquired}")

        # 如果锁获取成功，继续执行任务
        if not lock_acquired:
            # 如果锁获取失败，记录日志并重试
            # logger.info(f"Task {self.request.id} has locked, retrying...")
            raise task.retry(
                exc=Exception("Task rejected due to lock"),
                countdown=settings.task.task_default_retry_delay,
                max_retries=settings.task.task_retry_count,
            )

        try:

            # 成功获取锁后，继续执行任务
            instance = TaskService(self)
            return instance._run_30_seconds_task_with_locker()

        except Exception as e:
            # 如果执行过程中发生错误，记录日志并重试
            logger.error(
                f"Error while running task {task.request.id}: {e}",
                exc_info=settings.log.exc_info,
            )
            return f"Task failed: {str(e)}"
            

    def _run_30_seconds_task_with_locker(self) -> str:
        """实际的任务执行逻辑"""
        cache = CacheFactory.get_cache()

        try:
            # 执行你的实际任务逻辑
            for i in range(30):
                time.sleep(1)  # 模拟任务执行
                logger.info(f"Task {self.task.request.id} Seconds elapsed: {i + 1}")
                self.task.update_state(
                    state=states.STARTED, meta={"current": i + 1, "total": 30}
                )

            self.task.update_state(
                state=states.SUCCESS, meta={"message": "Task completed"}
            )
            return "Task completed"

        except Exception as e:
            # 任务执行过程中发生错误时
            err_msg = f"Error during task {self.task.request.id}: {e}"
            self.task.update_state(state=states.FAILURE, meta={"message": err_msg})
            raise Exception(err_msg)

        finally:
            # 确保任务结束后释放锁
            cache.release_lock(TASK_30S_SYNC_LOCK_KEY)

            # 确保任务结束后释放锁
            logger.info(f"Task: {self.task} finished.")

    @celery_app.task(bind=True)
    def run_with_connect_db(self):
        # db = sync_session_local()
        # 手动启动生成器
        with get_sync_db_session() as sync_db:
            try:
                # 获取数据库会话对象
                # 使用 db 进行数据库操作
                result = sync_db.query(User).limit(1).scalar()
                print("with auto operation:", result)
                sync_db.commit()
            except Exception as e:
                # 处理异常
                sync_db.rollback()
                raise e
            finally:
                # 手动关闭生成器
                logger.info("finally finished")

        return "connect db"
