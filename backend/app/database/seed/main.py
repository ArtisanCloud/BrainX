from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import settings
from app.database.seed.app import seed_apps
from app.database.seed.model_provider import seed_default_tenant_models
from app.database.seed.tenant import seed_tenants
from app.database.seed.user import seed_users

# 配置数据库连接字符串
SQLALCHEMY_DATABASE_URL = settings.database.dsn

# 创建异步数据库引擎
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# 创建一个异步会话类
async_session_local = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 初始化会话
async def start_seed() -> Exception | None:
    async with async_session_local() as async_db:
        await async_db.execute(text(f"SET search_path TO {settings.database.db_schema}, public"))
        try:
            #  执行添加root用户租户
            e = await seed_tenants(async_db)
            if e:
                raise e

            #  执行添加root用户种子
            e = await seed_users(async_db)
            if e:
                raise e

            # 执行添加种子数据的函数
            e = await seed_default_tenant_models(async_db)
            if e:
                raise e

            # 执行添加种子数据的函数
            e = await seed_apps(async_db)
            if e:
                raise e

            await async_db.commit()
            
        except Exception as e:
            await async_db.rollback()

            return e

        finally:
            await async_db.close()

        # await seed_conversations()

# 运行异步函数
if __name__ == "__main__":
    import asyncio

    asyncio.run(start_seed())
