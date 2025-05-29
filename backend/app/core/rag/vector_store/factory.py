from app import settings
from app.core.rag import FrameworkDriverType
from app.core.rag.vector_store.drivers.langchain.store import LangchainVectorStoreDriver
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType
from app.core.rag.vector_store.drivers.langchain.vdb.faiss.faiss import FaissVectorStore
from app.core.rag.vector_store.drivers.langchain.vdb.pgvector.pgvector import PGVectorStore
from app.core.rag.vector_store.interface import BaseVectorStore, VectorStoreDriver


class VectorStoreDriverFactory:
    @classmethod
    def create_vector_store_driver(
            cls,
            vdb_type: VectorStoreType,
            collection_name: str = "embedding",
            embedding_model: any = None,
    ) -> VectorStoreDriver:
        vdb = VDBFactory.create_vector_store(vdb_type, collection_name, embedding_model=embedding_model)

        return LangchainVectorStoreDriver(vdb)


class VDBFactory:
    @classmethod
    def create_vector_store(
            cls,
            vdb_type: VectorStoreType,
            collection_name: str = "embedding",
            embedding_model: any = None,
    ) -> BaseVectorStore:

        match vdb_type.value:
            case VectorStoreType.PGVECTOR.value:
                return PGVectorStore(settings.agent.pgvector, collection_name, embedding_model=embedding_model)
            case VectorStoreType.FAISS.value:
                return FaissVectorStore(1, None)
