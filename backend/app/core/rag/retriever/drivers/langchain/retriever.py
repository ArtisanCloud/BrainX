from typing import List, Optional, Any, Dict, Tuple

from langchain_postgres import PGVector

from app import settings
from app.core.ai_model.model_instance import ModelInstance
from app.core.rag import FrameworkDriverType
from app.core.rag.indexing.drivers.langchain.helper import convert_documents_to_nodes
from app.core.rag.retriever.interface import BaseRetriever
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType
from app.core.rag.vector_store.factory import VectorStoreDriverFactory
from app.core.rag.vector_store.interface import BaseVectorStore, VectorStoreDriver
from app.models.rag.document_node import DocumentNode


class LangchainRetriever(BaseRetriever):
    """
    Implementation of BaseRetriever for Langchain retriever.
    """

    def __init__(self,
                 vector_store_driver: VectorStoreDriver = None,
                 collection_name: str = "rag_embeddings",
                 embedding_model_instance: Optional[ModelInstance] = None,
                 ):
        super().__init__()

        self.vector_stored_driver: VectorStoreDriver | None = None
        if vector_store_driver is None:
            embedding_model = embedding_model_instance.model.get_provider_model()
            # get vector store
            self.vector_stored_driver = VectorStoreDriverFactory.create_vector_store_driver(
                FrameworkDriverType(settings.agent.framework_driver),
                VectorStoreType(settings.agent.vdb),
                collection_name=collection_name,
                embedding_model=embedding_model
            )
        else:
            self.vector_stored_driver = vector_store_driver

        self.vector_store = (
            self.vector_stored_driver.
            get_base_vector_store().
            get_vector_store()
        )
        self.retriever = self.vector_store.as_retriever()

    def retrieve(self, query: str, top_k: int, filters: Dict = None, **kwargs: Any) -> Tuple[
        List[DocumentNode] | None, Exception | None]:

        try:
            list_documents = self.retriever.similarity_search(input, kwargs=kwargs)

            list_nodes = convert_documents_to_nodes(list_documents)

            return list_nodes, None

        except Exception as e:
            return None, e


def get_base_vector_store(self) -> BaseVectorStore:
    return self.vector_stored_driver.get_base_vector_store()
