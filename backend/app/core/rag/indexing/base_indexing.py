from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from app.core.rag.indexing.dataset import Dataset


class BaseIndexing(ABC):
    """Abstract base class for indexing and retrieval functionality."""

    @abstractmethod
    def retrieve(self, retrival_method: str, query: str, dataset: Dataset, top_k: int,
                 score_threshold: float, reranking_model: Dict) -> Dataset:
        """Retrieve documents from the dataset based on the retrieval method and query."""
        raise NotImplementedError

    @abstractmethod
    def clean(self, dataset: Dataset, node_ids: Optional[List[str]] = None, with_keywords: bool = True):
        """Clean up index entries associated with the dataset."""
        raise NotImplementedError

    @abstractmethod
    def transform(self, documents: Dataset, **kwargs) -> Dataset:
        """Transform the retrieved documents."""
        raise NotImplementedError

    def _get_splitter(self, processing_rule: Dict, embedding_model_instance: Optional[Any] = None):
        """
        Get the text splitter based on processing rules.
        """
        raise NotImplementedError

