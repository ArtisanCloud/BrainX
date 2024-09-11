from typing import List, Optional, Tuple, Dict

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.indices.vector_store import VectorIndexRetriever

from app.core.brainx.indexing.engine import generate_storage_context, get_service_context
from app.core.rag.retrieval.interface import BaseRetriever
from app.models import Document
from app.models.rag.document_node import DocumentNode


class LlamaIndexRetriever(BaseRetriever):
    """
    Implementation of BaseRetriever for LlamaIndex retrieval.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the LlamaIndexRetriever with optional configuration.

        Args:
            config (Optional[dict]): Optional configuration dictionary for the retrieval.
        """
        self.config = config or {}
        # Initialize LlamaIndex resources
        self.index = self._initialize_retriever()

    def _initialize_retriever(self):
        """
        Private method to initialize the LlamaIndex retrieval.

        Returns:
            An retrieval object.
        """
        # Implement retrieval initialization logic
        # For example, return a new instance of LlamaIndex
        pass

    def retrieve(self, query: str, top_k: int, filters: Dict = None) -> Tuple[
        List[DocumentNode] | None, Exception | None]:
        try:

            # 存储上下文
            storage_context = generate_storage_context(self.vector_store)

            # 服务上下文
            service_context = get_service_context(self.llm)

            index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=storage_context,
                service_context=service_context
            )

            # configure retrieval
            retriever = VectorIndexRetriever(
                index=index,
                similarity_top_k=top_k,
            )

            # configure response synthesizer
            response_synthesizer = get_response_synthesizer()

            match_docs = retriever.retrieve(content)
            # print(match_docs)

            return (
                list(Document(
                    page_content=doc.node.text,
                    metadata={
                        'score': doc.score,
                        'node_id': doc.node_id,
                        'metadata': doc.node.metadata
                    },
                ) for doc in match_docs),
                None
            )

        except Exception as e:
            return None, e
