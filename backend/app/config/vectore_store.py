from pydantic import BaseModel

from app.core.rag import FrameworkDriverType
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType


class VectorStore(BaseModel):
    frame_driver: str = FrameworkDriverType.LANGCHAIN.value
    vdb: str = VectorStoreType.PGVECTOR.value

