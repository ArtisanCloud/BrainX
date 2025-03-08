from pydantic import BaseModel

from app.config.agent.pgvector import PGVector
from app.core.rag import FrameworkDriverType
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType


class Agent(BaseModel):
    framework_driver: str = FrameworkDriverType.LANGCHAIN.value
    vdb: str = VectorStoreType.PGVECTOR.value
    vector_store_table_name: str = "langchain_pg_embedding"
    vector_store_collection: str = "rag_embeddings"
    router_llm: str
    pgvector: PGVector

