from contextlib import contextmanager

from sqlalchemy import text
from sqlalchemy.orm import Session

from app import settings
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_local, sync_session_local

"""
| 场景                     | 如何获取 Session                        | 是否需要 `commit/rollback` |
| ---------------------- | ----------------------------------- | ---------------------- |
| FastAPI（异步）            | `Depends(get_async_db_session_dep)` | ❌ 不需要，已自动处理            |
| Celery、脚本等（同步）         | `with get_sync_db_session_dep()`    | ❌ 不需要，已自动处理            |
| 直接调用 `session_local()` | ✅ 必须手动 commit/rollback/close        |                        |
"""


async def get_async_db_session_dep() -> AsyncSession:
    from app.api.context_manager import context_set_db_session_rollback

    async with async_session_local() as async_db:
        await async_db.execute(
            text(f"SET search_path TO {settings.database.db_schema}, public")
        )

        try:
            yield async_db
            #  commit the db session if no exception occurs
            #  if context_set_db_session_rollback is set to True then rollback the db session
            if context_set_db_session_rollback.get():
                logger.error("Rollback Async DB dep session")
                await async_db.rollback()
            else:
                logger.info("Commit Async DB dep session")
                await async_db.commit()
        except Exception as e:
            #  rollback the db session if any exception occurs
            logger.error(f"Async Session dep error: {e}")
            await async_db.rollback()
            raise e

        # No need for `await db.close()` since context manager handles it
        # finally:
        #  close the db session
        # await db.close()


@contextmanager
# 为了某些场景，比如 Celery 等需要直接调用的场景，你可以使用一个简单的函数来获取 session：
def get_sync_db_session_dep() -> Session:
    sync_db = sync_session_local()
    if not sync_db:
        raise ValueError("Failed to initialize sync session")

    sync_db.execute(text(f"SET search_path TO {settings.database.db_schema}, public"))
    # 外层一定要用 with 才能让这个上下文管理器的功能生效。
    # 如果直接调用 get_sync_db_session_dep() 而不使用 with，except 和 finally 块中的代码将不会被执行，
    # 而是需要自己去维护commit，rollback，close
    # 因为生成器会在 yield db 处暂停，直到被显式地继续执行。

    try:
        yield sync_db
        # 提交事务

        logger.info("Sync DB dep commit")
        sync_db.commit()
    except Exception as e:
        # 出现异常时回滚事务
        logger.error("Sync DB dep rollback")
        sync_db.rollback()
        raise e
    finally:
        # 关闭数据库会话

        logger.info("Sync DB dep session closed")
        sync_db.close()

