from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from app.config.config import settings
from pytz import timezone


def get_database_sync_url():
    async_db_url = settings.database.dsn
    sync_db_url = async_db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")

    return sync_db_url


COMMON_CONFIG = {
    "pool_recycle": settings.database.pool_recycle,  # 连接最大生命周期（秒）
    "pool_pre_ping": settings.database.pool_pre_ping,
}

async_db_engine = create_async_engine(
    settings.database.dsn,
    connect_args={
        "server_settings": {
            "application_name": "brainx"  # Correct way to add application_name for asyncpg
        }
    },    
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,  # 连接池获取连接的超时时间（秒）
    echo=settings.database.echo,  # 输出 SQL 日志
    **COMMON_CONFIG  # 传递通用配置
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
    poolclass=NullPool,  # 明确指定 NullPool 防止同步连接池复用连接
    **COMMON_CONFIG  # 传递通用配置
)

sync_session_local = sessionmaker(
    bind=sync_engine, 
    autocommit=False, 
    autoflush=False, 
    class_=Session
)
