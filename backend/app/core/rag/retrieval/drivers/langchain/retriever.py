from typing import List, Optional, Any, Dict, Tuple

from langchain_postgres import PGVector

from app import settings
from app.logger import logger
from app.core.ai_model.model_instance import ModelInstance
from app.core.rag import FrameworkDriverType
from app.core.rag.ingestion.drivers.langchain.helper import convert_documents_to_nodes, \
    convert_documents_to_nodes_with_score
from app.core.rag.retrieval.interface import BaseRetriever
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType
from app.core.rag.vector_store.factory import VectorStoreDriverFactory
from app.core.rag.vector_store.interface import BaseVectorStore, VectorStoreDriver
from app.models.rag.document_node import DocumentNode


class LangchainRetriever(BaseRetriever):
    """
    Implementation of BaseRetriever for Langchain retrieval.
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

    def invoke(self, query: str, top_k: int, score_threshold: float, filters: Dict = None, **kwargs: Any) -> Tuple[
        List[DocumentNode] | None, Exception | None]:
        try:

            retriever = self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                # search_type="mmr",
                search_kwargs={
                    "k": top_k,
                    "score_threshold": score_threshold,
                    "filter": filters
                }
            )
            list_documents = retriever.invoke(query)
            # print(list_documents)
            list_nodes = convert_documents_to_nodes(list_documents)

            return list_nodes, None

        except Exception as e:
            logger.info(f"Error in invoking documents: {e}", exc_info=settings.log.exc_info)
            return None, e

    def retrieve(self, query: str, top_k: int, score_threshold: float = None, filters: Dict = None, **kwargs: Any) -> \
    Tuple[
        List[DocumentNode] | None, Exception | None]:

        try:

            list_documents = self.vector_store.similarity_search_with_relevance_scores(
                query,
                k=top_k,
                score_threshold=score_threshold,
                filter=filters
            )
            # print(list_documents)
            list_nodes = convert_documents_to_nodes_with_score(list_documents)

            return list_nodes, None

        except Exception as e:
            logger.info(f"Error in retrieving documents: {e}", exc_info=settings.log.exc_info)
            return None, e


def get_base_vector_store(self) -> BaseVectorStore:
    return self.vector_stored_driver.get_base_vector_store()
