from app.core.rag import FrameworkDriverType
from app.core.rag.vector_store.drivers.langchain.store import LangchainVectorStore
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType
from app.core.rag.vector_store.drivers.langchain.vdb.faiss.faiss import FaissVectorStoreDriver
from app.core.rag.vector_store.drivers.langchain.vdb.pgvector.pgvector import PGVectorStoreDriver
from app.core.rag.vector_store.drivers.llamaindex.store import LLamaIndexVectorStore
from app.core.rag.vector_store.interface import BaseVectorStore

class VectorStoreFactory:
    @classmethod
    def create_vector_store(cls, framework_type: FrameworkDriverType, vdb_type: VectorStoreType) -> BaseVectorStore:

        vdb_instance = VDBFactory.create_vector_store(vdb_type)

        if framework_type.value == FrameworkDriverType.LANGCHAIN:
            return LangchainVectorStore(vdb_instance)

        elif framework_type.value == FrameworkDriverType.LLAMA_INDEX:
            return LLamaIndexVectorStore(vdb_instance)
        else:
            raise ValueError(f"Unknown framework: {framework_type.value}")


class VDBFactory:
    @classmethod
    def create_vector_store(cls, vdb_type: VectorStoreType) -> BaseVectorStore:

        match vdb_type.value:
            case VectorStoreType.PGVECTOR.value:
                return PGVectorStoreDriver("", "rag_embeddings")
            case VectorStoreType.FAISS.value:
                return FaissVectorStoreDriver(1, None)

