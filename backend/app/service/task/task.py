import time
from typing import Any

from sqlalchemy import text, update, UUID
from sqlalchemy.orm import Session

from app.database.deps import get_sync_db_session
from app.database.seed import init_user_uuid
from app.database.session import sync_session_local
from app.logger import logger
from app.models import User
from app.service.task.celery_app import celery_app


@celery_app.task
def run_manual_connect_db():
    # 手动启动生成器
    db = sync_session_local()

    try:
        # 获取数据库会话对象
        # 使用 db 进行数据库操作
        result = db.query(User).limit(1).scalar()
        print("manual operation:", result)
        db.commit()
    except Exception as e:
        # 处理异常
        db.rollback()
        raise e

    finally:
        db.close()
        # 手动关闭生成器
        logger.info("finally finished")

    return "connect db"


class TaskService:

    def __init__(self, task: Any):
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
            logger.info(f"Seconds elapsed: {i + 1}")
            self.task.update_state(state='PROGRESS', meta={'current': i + 1, 'total': 30})
        return "Task completed"

    @celery_app.task(bind=True)
    def run_with_connect_db(self):
        # db = sync_session_local()
        # 手动启动生成器
        with get_sync_db_session() as db:
            try:
                # 获取数据库会话对象
                # 使用 db 进行数据库操作
                result = db.query(User).limit(1).scalar()
                print("with auto operation:", result)
                # db.commit()
            except Exception as e:
                # 处理异常
                raise e
            finally:
                # 手动关闭生成器
                logger.info("finally finished")

        return "connect db"
