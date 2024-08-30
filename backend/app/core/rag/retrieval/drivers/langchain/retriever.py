from typing import List, Optional, Any

from langchain_postgres import PGVector

from app.core.rag.indexing.drivers.langchain.helper import convert_documents_to_nodes
from app.core.rag.retrieval.interface import RetrieverDriver
from app.core.rag.vector_store.interface import BaseVectorStore
from app.models import Document
from app.models.rag.document_node import DocumentNode


class LangchainRetrieverDriver(RetrieverDriver):
    """
    Implementation of BaseRetriever for Langchain retrieval.
    """

    def __init__(self, vector_store: BaseVectorStore):
        super().__init__()

        self.vector_store: PGVector = vector_store.get_vector_store()
        self.retriever = self.vector_store.as_retriever()

    def invoke(self, input: str, config: Optional[Any] = None, **kwargs: Any) -> List[DocumentNode]:

        try:
            list_documents = self.retriever.invoke(input, config=config, kwargs=kwargs)
            list_nodes = convert_documents_to_nodes(list_documents)

            return list_nodes
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve documents: {e}")
