from pydantic import BaseModel

from app.config.agent.pgvector import PGVector
from app.core.rag import FrameworkDriverType
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType


class Agent(BaseModel):
    framework_driver: str = FrameworkDriverType.LANGCHAIN.value
    vdb: str = VectorStoreType.PGVECTOR.value
    pgvector: PGVector
