import pytest
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import settings
from app.models import Document
from app.main import app

# TEST_DATABASE_URL = settings.test.db_url
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(
    TEST_DATABASE_URL,
    # echo=True,
    echo=False,
)  # 设置 echo=False 以禁用日志记录
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest.fixture
async def db():
    async with engine.begin() as conn:
        # 清除所有表
        await conn.run_sync(Document.metadata.drop_all)
        # 创建表
        await conn.run_sync(Document.metadata.create_all)
    async with async_session() as session:
        yield session
    async with engine.begin() as conn:
        # 清理表
        await conn.run_sync(Document.metadata.drop_all)
