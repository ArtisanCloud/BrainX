import os
from typing import cast

from starlette.staticfiles import StaticFiles

from app import default_local_storage_path
from app.logger import logger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from alembic.config import Config
from alembic import script
from alembic.runtime import migration
from sqlalchemy.engine import create_engine, Engine

from app.api.api import api_router
from app.database.wait_for_db import check_database_connection
from app.core.config import settings, AppEnvironment

from contextlib import asynccontextmanager

from app.core.brain.indexing.pg_vector import get_vector_store_singleton, CustomPGVectorStore
from app.openapi.openapi import openapi_router
from server import start


# 检查当前数据库版本
def check_current_head(alembic_cfg: Config, connectable: Engine) -> bool:
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    # print("-----", directory)
    with connectable.begin() as connection:
        print(connection)
        context = migration.MigrationContext.configure(connection)
        # print("-----", context)
        # print(123, set(context.get_current_heads()), 543, set(directory.get_heads()))
        return set(context.get_current_heads()) == set(directory.get_heads())


# 设置监控服务
def __setup_sentry():
    if settings.sentry.dsn:
        logger.info("Setting up Sentry")
        if settings.server.environment == AppEnvironment.PRODUCTION:
            profiles_sample_rate = None
        else:
            profiles_sample_rate = settings.sentry.sample_rate
        # sentry_sdk.init(
        #     dsn=settings.SENTRY_DSN,
        #     environment=settings.server.environment,
        #     release=settings.RENDER_GIT_COMMIT,
        #     debug=settings.VERBOSE,
        #     traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        #     profiles_sample_rate=profiles_sample_rate,
        # )
        # else:
        logger.info("Skipping Sentry setup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # first wait for DB to be connectable
    await check_database_connection()
    cfg = Config("alembic.ini")
    # Change DB URL to use psycopg2 driver for this specific check
    db_url = settings.database.url.replace(
        "postgresql+asyncpg://", "postgresql+psycopg2://"
    )
    cfg.set_main_option("sqlalchemy.url", db_url)
    engine = create_engine(db_url, echo=True)
    # print("robot_chat:", robot_chat)
    if not check_current_head(cfg, engine):
        raise Exception(
            "Database is not up to date. Please run `poetry run alembic upgrade head`"
        )

    # initialize pg vector store singleton
    query_embedding_table = settings.database.table_name_vector_store
    vector_store, _ = get_vector_store_singleton(query_embedding_table)
    vector_store = cast(CustomPGVectorStore, vector_store)
    await vector_store.run_setup()

    # try:
    #     # Some setup is required to initialize the llama-indexing sentence splitter
    #     split_by_sentence_tokenizer()
    # except FileExistsError:
    #     # Sometimes seen in deployments, should be benign.
    #     logger.info("Tried to re-download NLTK files but already exists.")
    yield
    # This section is run on app shutdown
    await vector_store.close()


app = FastAPI(
    title=settings.server.project_name,
    openapi_url=f"{settings.api.api_prefix}/openapi.json",

    # https://fastapi.tiangolo.com/advanced/events/
    # You can define logic (code) that should be executed before the application starts up.
    # This means that this code will be executed once, before the application starts receiving requests.
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=os.path.abspath(default_local_storage_path)), name="statics")


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]
if settings.server.cors_origins:
    # 添加其他允许的来源
    origins.extend(settings.server.cors_origins)

# print("cors with domain", origins)

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="session_key")
# 允许所有方法和请求头
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api.api_prefix)
app.include_router(openapi_router, prefix=settings.api.openapi_prefix)

if __name__ == '__main__':
    start()
