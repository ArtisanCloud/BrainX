from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


from app.models import Document, DocumentSegment, Dataset


class IndexingInterface(ABC):
    """Abstract base class for indexing and retrieval functionality."""

    def load_data(self, dataset: Dataset):
        """加载原始数据"""
        pass

    def split_data(self, documents: List[Document]) -> List[DocumentSegment]:
        """将文档拆分为较小的块"""
        pass

    def store_data(self, data_chunks: List[DocumentSegment]):
        """将数据块存储到索引中"""
        pass
