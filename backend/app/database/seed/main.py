from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import settings
from app.database.seed.app import seed_apps
from app.database.seed.model_provider import seed_model_providers
from app.database.seed.tenant import seed_tenants
from app.database.seed.user import seed_users

# 配置数据库连接字符串
SQLALCHEMY_DATABASE_URL = settings.database.async_url

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
    async with async_session_local() as db:
        try:
            #  执行添加root用户租户
            e = await seed_tenants(db)
            if e:
                raise e

            #  执行添加root用户种子
            e = await seed_users(db)
            if e:
                raise e

            # 执行添加种子数据的函数
            e = await seed_model_providers(db)
            if e:
                raise e

            # 执行添加种子数据的函数
            e = await seed_apps(db)
            if e:
                raise e

            await db.commit()
            
        except Exception as e:
            await db.rollback()

            return e

        finally:
            await db.close()

        # await seed_conversations()

# 运行异步函数
if __name__ == "__main__":
    import asyncio

    asyncio.run(start_seed())
