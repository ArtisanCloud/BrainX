from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_local, sync_session_local


async def get_async_db_session() -> AsyncSession:
    from app.api.context_manager import context_set_db_session_rollback
    async with async_session_local() as db:
        try:
            yield db
            #  commit the db session if no exception occurs
            #  if context_set_db_session_rollback is set to True then rollback the db session
            if context_set_db_session_rollback.get():
                logger.info('rollback db session')
                await db.rollback()
            else:
                await db.commit()
        except Exception as e:
            #  rollback the db session if any exception occurs
            logger.error(f"session local error: {e}")
            await db.rollback()

        finally:
            #  close the db session
            await db.close()


@contextmanager
# 为了某些场景，比如 Celery 等需要直接调用的场景，你可以使用一个简单的函数来获取 session：
def get_sync_db_session() -> Session:
    db = sync_session_local()
    # 外层一定要用 with 才能让这个上下文管理器的功能生效。
    # 如果直接调用 get_sync_db_session() 而不使用 with，except 和 finally 块中的代码将不会被执行，
    # 而是需要自己去维护commit，rollback，close
    # 因为生成器会在 yield db 处暂停，直到被显式地继续执行。

    try:
        yield db
        # 提交事务
        if db:
            print("sync db commit")
            db.commit()
    except Exception as e:
        # 出现异常时回滚事务
        if db:
            print("sync db rollback")
            db.rollback()
        raise e
    finally:
        # 关闭数据库会话
        if db:
            print("sync db closed")
            db.close()
