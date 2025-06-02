from contextlib import contextmanager

from sqlalchemy import text
from sqlalchemy.orm import Session

from app import settings
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_local, sync_session_local

"""
| 场景                                    | 当前是否自动 commit/rollback | 是否需要手动控制 |
| ------------------------------------- | ---------------------- | -------- |
| FastAPI + `get_async_db_session()`    | ❌ 否                    | ✅ 需要     |
| 脚本 / Celery + `get_sync_db_session()` | ❌ 否                    | ✅ 需要     |

"""


async def get_async_db_session() -> AsyncSession:
    from app.api.context_manager import context_set_db_session_rollback

    async with async_session_local() as async_db:
        async_db._from_manual_session = True  # 自定义标记

        await async_db.execute(
            text(f"SET search_path TO {settings.database.db_schema}, public")
        )
        yield async_db
        # 需要在外部with域中调用commit或者rollback
        # No need for `await db.close()` since context manager handles it
        # finally:
        #  close the db session
        # await db.close()


@contextmanager
# 为了某些场景，比如 Celery 等需要直接调用的场景，你可以使用一个简单的函数来获取 session：
def get_sync_db_session() -> Session:
    sync_db = sync_session_local()
    sync_db._from_manual_session = True  # 自定义标记

    if not sync_db:
        raise ValueError("Failed to initialize sync session")

    sync_db.execute(text(f"SET search_path TO {settings.database.db_schema}, public"))
    # 外层一定要用 with 才能让这个上下文管理器的功能生效。
    # 如果直接调用 get_sync_db_session_dep() 而不使用 with，except 和 finally 块中的代码将不会被执行，
    # 而是需要自己去维护commit，rollback，close
    # 因为生成器会在 yield db 处暂停，直到被显式地继续执行。

    try:
        yield sync_db
        # 需要在外部with域中调用commit或者rollback
    finally:
        # 关闭数据库会话
        logger.info("Sync DB session closed")
        sync_db.close()


# 判断 db 是否为 FastAPI 依赖注入提供的对象
def is_manual_session(db: Session | AsyncSession) -> bool:
    return getattr(db, "_from_manual_session", False)
