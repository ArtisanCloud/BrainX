import os
import sys

import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from alembic.config import Config
import alembic.config
from alembic import script
from alembic.runtime import migration
from sqlalchemy.engine import create_engine, Engine

from app.api.api import api_router
from app.db.wait_for_db import check_database_connection
from app.core.config import settings, AppEnvironment

from contextlib import asynccontextmanager

import sentry_sdk

# from app.qa.pg_vector import get_vector_store_singleton, CustomPGVectorStore


# 获取当前日志记录器
logger = logging.getLogger(__name__)


# 检查当前数据库版本
def check_current_head(alembic_cfg: Config, connectable: Engine) -> bool:
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


def __setup_logging(log_level: str, log_file_path: str):
    log_level = getattr(logging, log_level.upper())
    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)
    logger.info("Set up logging with log level %s", log_level)


# 设置监控服务
def __setup_sentry():
    if settings.SENTRY_DSN:
        logger.info("Setting up Sentry")
        if settings.ENVIRONMENT == AppEnvironment.PRODUCTION:
            profiles_sample_rate = None
        else:
            profiles_sample_rate = settings.SENTRY_SAMPLE_RATE
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT.value,
            release=settings.RENDER_GIT_COMMIT,
            debug=settings.VERBOSE,
            traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
            profiles_sample_rate=profiles_sample_rate,
        )
    else:
        logger.info("Skipping Sentry setup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # first wait for DB to be connectable
    await check_database_connection()
    cfg = Config("alembic.ini")
    # Change DB URL to use psycopg2 driver for this specific check
    db_url = settings.DATABASE_URL.replace(
        "postgresql+asyncpg://", "postgresql+psycopg2://"
    )
    cfg.set_main_option("sqlalchemy.url", db_url)
    engine = create_engine(db_url, echo=True)
    # print("engine:", engine)
    if not check_current_head(cfg, engine):
        raise Exception(
            "Database is not up to date. Please run `poetry run alembic upgrade head`"
        )

    yield

    # # initialize pg vector store singleton
    # vector_store = await get_vector_store_singleton()
    # vector_store = cast(CustomPGVectorStore, vector_store)
    # await vector_store.run_setup()
    #
    # try:
    #     # Some setup is required to initialize the llama-index sentence splitter
    #     split_by_sentence_tokenizer()
    # except FileExistsError:
    #     # Sometimes seen in deployments, should be benign.
    #     logger.info("Tried to re-download NLTK files but already exists.")
    # yield
    # # This section is run on app shutdown
    # await vector_store.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",

    # https://fastapi.tiangolo.com/advanced/events/
    # You can define logic (code) that should be executed before the application starts up.
    # This means that this code will be executed once, before the application starts receiving requests.
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    origins = settings.BACKEND_CORS_ORIGINS.copy()

    origins.append([
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000"
    ])
    # allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_PREFIX)
# app.mount(f"/{settings.LOADER_IO_VERIFICATION_STR}", loader_io_router)


def start():
# if __name__ == '__main__':

    print("Running in AppEnvironment: " + settings.ENVIRONMENT.value)
    __setup_logging(settings.LOG_LEVEL, "logs/app.log")
    __setup_sentry()
    """Launched with `poetry run start` at root level"""

    if settings.RENDER:
        # on render.com deployments, run migrations
        logger.debug("Running migrations")
        alembic_args = ["--raiseerr", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        logger.debug("Migrations complete")
    else:
        logger.debug("Skipping migrations")

    live_reload = not settings.RENDER

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=live_reload,
        workers=settings.UVICORN_WORKER_COUNT,
    )
