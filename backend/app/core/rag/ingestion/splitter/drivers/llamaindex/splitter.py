from typing import Optional, Any, Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.rag.ingestion.splitter.base import BaseTextSplitter
from app.models.rag.document_node import DocumentNode


class LlamaIndexRecursiveCharacterTextSplitter(BaseTextSplitter, RecursiveCharacterTextSplitter):
    def __init__(self, separator: str = "\n\n", separators: Optional[list[str]] = None, **kwargs: Any):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self.separator = separator
        self._separators = separators or ["\n\n", "\n", " ", ""]

    def split_documents(self, documents: Iterable[DocumentNode]) -> list[DocumentNode]:
        print("llamaindex split documents:", documents)
        return []
