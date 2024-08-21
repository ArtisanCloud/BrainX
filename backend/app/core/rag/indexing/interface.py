from abc import ABC, abstractmethod
from typing import List, Tuple

from app.models.rag.document_node import DocumentNode


class BaseIndexing(ABC):

    @abstractmethod
    def transform_documents(self, segments: List[DocumentNode]) -> List[DocumentNode]:
        raise NotImplementedError

