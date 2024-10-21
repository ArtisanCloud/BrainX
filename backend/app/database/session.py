from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from app.config.config import settings
from pytz import timezone

echo_log = settings.database.echo_log


def get_database_sync_url():
    async_db_url = settings.database.async_url
    sync_db_url = async_db_url.replace(
        "postgresql+asyncpg://", "postgresql+psycopg://"
    )

    return sync_db_url


async_db_engine = create_async_engine(
    settings.database.async_url,
    pool_pre_ping=True,
    pool_size=4,
    max_overflow=4,
    pool_recycle=3600,
    pool_timeout=120,
    echo=echo_log,
)

async_session_local = async_sessionmaker(
    bind=async_db_engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession
)

# Synchronous session maker for Celery
sync_engine = create_engine(
    get_database_sync_url(),  # 这里用你的实际数据库 URL
    poolclass=NullPool,
    echo=echo_log,
)

sync_session_local = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    class_=Session
)

UTC = timezone('UTC')
