from contextlib import contextmanager

from sqlalchemy import text
from sqlalchemy.orm import Session

from app import settings
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_local, sync_session_local


async def get_async_db_session() -> AsyncSession:
    from app.api.context_manager import context_set_db_session_rollback

    async with async_session_local() as db:
        await db.execute(
            text(f"SET search_path TO {settings.database.db_schema}, public")
        )

        try:
            yield db
            #  commit the db session if no exception occurs
            #  if context_set_db_session_rollback is set to True then rollback the db session
            if context_set_db_session_rollback.get():
                logger.info("Rollback Async DB session")
                await db.rollback()
            else:
                await db.commit()
        except Exception as e:
            #  rollback the db session if any exception occurs
            logger.error(f"Asyanc Session local error: {e}")
            await db.rollback()
            raise e

        # No need for `await db.close()` since context manager handles it
        # finally:
        #  close the db session
        # await db.close()


@contextmanager
# 为了某些场景，比如 Celery 等需要直接调用的场景，你可以使用一个简单的函数来获取 session：
def get_sync_db_session() -> Session:
    db = sync_session_local()
    if not db:
        raise ValueError("Failed to initialize sync session")

    db.execute(text(f"SET search_path TO {settings.database.db_schema}, public"))
    # 外层一定要用 with 才能让这个上下文管理器的功能生效。
    # 如果直接调用 get_sync_db_session() 而不使用 with，except 和 finally 块中的代码将不会被执行，
    # 而是需要自己去维护commit，rollback，close
    # 因为生成器会在 yield db 处暂停，直到被显式地继续执行。

    try:
        yield db
        # 提交事务

        logger.info("Sync DB commit")
        db.commit()
    except Exception as e:
        # 出现异常时回滚事务
        logger.error("Sync DB rollback")
        db.rollback()
        raise e
    finally:
        # 关闭数据库会话

        logger.info("Sync DB session closed")
        db.close()
