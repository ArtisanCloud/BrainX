from abc import ABC, abstractmethod
from typing import List

from app.models import Document, DocumentSegment, Dataset


class IndexingInterface(ABC):
    """Abstract base class for indexing and retrieval functionality."""

    @abstractmethod
    def load_data(self, dataset: Dataset):
        """Load raw data."""
        pass

    @abstractmethod
    def split_data(self, documents: List[Document]) -> List[DocumentSegment]:
        """Split documents into smaller chunks."""
        pass

    @abstractmethod
    def store_data(self, data_chunks: List[DocumentSegment]):
        """Store data chunks into the index."""
        pass
