from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.models import Document
from app.models.rag.document_node import DocumentNode


class BaseRetriever(ABC):
    """
    Define the retriever interface.
    """

    @abstractmethod
    def invoke(self, input: str, config: Optional[Any] = None, **kwargs: Any) -> List[DocumentNode]:
        raise NotImplementedError


class RetrieverDriver(ABC):
    pass
