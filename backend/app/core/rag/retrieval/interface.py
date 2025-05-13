from abc import ABC
from typing import List, Tuple, Dict

from app.models.rag.document_node import DocumentNode


class BaseRetriever(ABC):
    """
    Define the retrieval interface.
    """
    def __init__(self):
        self.search_type = "similarity"

    nodes: List[DocumentNode]
    """List of documents to retrieve from."""
    k: int
    """Number of top results to return"""

    def __init__(self):
        self.vector_store = None

    def get_vector_store(self) -> any:
        return self.vector_store

    def retrieve(self, query: str, top_k: int=3, score_threshold: float=0.5, filters: Dict = None) -> Tuple[
        List[DocumentNode] | None, Exception | None]:
        pass
