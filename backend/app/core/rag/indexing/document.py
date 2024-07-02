from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class BaseDocument(ABC, BaseModel):
    """Abstract class for storing a piece of text and associated metadata."""

    page_content: str
    """String text content of the document."""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    """Arbitrary metadata about the page content (e.g., source, relationships to other documents, etc.)."""

    type: str = "Document"
    """Type identifier for the document."""

    score: Optional[float] = None
    """Score associated with the document, if any."""

    node_id: Optional[str] = None
    """Unique identifier for the node."""

    embedding: Optional[List[float]] = None
    """Optional embedding vector for the document."""

    def __init__(self, page_content: str, **kwargs: Any) -> None:
        """Initialize a Document with page content and optional metadata."""
        super().__init__(page_content=page_content, **kwargs)

    @abstractmethod
    def get_score(self, raise_error: bool = False) -> float:
        """Get score."""
        raise NotImplementedError

    @abstractmethod
    def get_content(self) -> str:
        """Get the content of the document."""
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get the metadata of the document."""
        raise NotImplementedError

    @abstractmethod
    def get_embedding(self) -> Optional[List[float]]:
        """Get the embedding of the document."""
        raise NotImplementedError

    @abstractmethod
    def set_score(self, score: float) -> None:
        """Set the score for the document."""
        raise NotImplementedError

    @abstractmethod
    def set_embedding(self, embedding: List[float]) -> None:
        """Set the embedding for the document."""
        raise NotImplementedError

    @abstractmethod
    def update_metadata(self, new_metadata: Dict[str, Union[str, int, float]]) -> None:
        """Update the metadata with new values."""
        raise NotImplementedError

    @abstractmethod
    async def get_embedding_async(self) -> Optional[List[float]]:
        """Get the embedding of the document asynchronously."""
        raise NotImplementedError

    def __str__(self) -> str:
        score_str = "None" if self.score is None else f"{self.score: 0.3f}"
        return f"Document:\nContent: {self.page_content}\nScore: {score_str}\nMetadata: {self.metadata}"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    @abstractmethod
    def is_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        raise NotImplementedError

    @abstractmethod
    def process_document(self) -> None:
        """Abstract method to process the document, to be implemented by subclasses."""
        raise NotImplementedError
