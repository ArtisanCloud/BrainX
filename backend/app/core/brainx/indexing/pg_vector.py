from typing import Tuple

from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy.engine import make_url
from app.database.session import async_session_local as app_async_session_local, async_db_engine as app_engine
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

singleton_instances = {}
did_run_setup = False


class CustomPGVectorStore(PGVectorStore):
    """
    Custom PGVectorStore that uses the same connection pool as the FastAPI app.
    """

    def _connect(self) -> None:
        self._engine = create_engine(self.connection_string)
        self._session = sessionmaker(self._engine)

        # Use our existing app engine and session so we can use the same connection pool
        self._async_engine = app_engine
        self._async_session = app_async_session_local

    async def close(self) -> None:
        self._session.close_all()
        self._engine.dispose()

        await self._async_engine.dispose()

    def _create_tables_if_not_exists(self) -> None:
        pass

    def _create_extension(self) -> None:
        pass

    async def run_setup(self) -> None:
        global did_run_setup
        if did_run_setup:
            return
        self._initialize()
        async with self._async_session() as session:
            async with session.begin():
                statement = sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector")
                await session.execute(statement)
                await session.commit()

        async with self._async_session() as session:
            async with session.begin():
                conn = await session.connection()
                await conn.run_sync(self._base.metadata.create_all)
        did_run_setup = True


def get_vector_store_singleton(table_name: str) -> Tuple[BasePydanticVectorStore | None, Exception | None]:
    global singleton_instances

    if table_name == '':
        return None, Exception("Table name cannot be empty")

    instance = singleton_instances.get(table_name)
    if instance is not None:
        return instance, None

    try:
        url = make_url(settings.database.async_url)
        singleton_instances[table_name] = CustomPGVectorStore.from_params(
            host=url.host,
            port=url.port or 5432,
            database=url.database,
            user=url.username,
            password=url.password,
            table_name=table_name,
            embed_dim=768,
        )
    except Exception as e:
        return None, e

    return singleton_instances[table_name], None
