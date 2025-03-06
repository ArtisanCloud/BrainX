import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import settings
from app.models import Document


TEST_DATABASE_URL = settings.test.db_url
# TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(
    TEST_DATABASE_URL,
    # echo=True,
    echo=False,
)  # 设置 echo=False 以禁用日志记录
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest.fixture
async def db():
    # 在每个测试开始前创建数据库连接
    async with engine.begin() as conn:
        await conn.run_sync(Document.metadata.create_all)

    async with async_session() as session:
        yield session  # 返回会话供测试使用

    # 在测试后回滚事务
    async with async_session() as session:
        await session.rollback()

    # 测试结束后关闭数据库连接
    await engine.dispose()
