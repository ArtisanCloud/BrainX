from typing import Optional, Any, Iterable, List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.rag.ingestion.extractor.base import Block
from app.core.rag.ingestion.splitter.base import BaseTextSplitter
from app.models.rag.document_node import DocumentNode


class LlamaIndexRecursiveCharacterTextSplitter(BaseTextSplitter, RecursiveCharacterTextSplitter):
    def __init__(self, separator: str = "\n\n", separators: Optional[list[str]] = None, **kwargs: Any):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self.separator = separator
        self._separators = separators or ["\n\n", "\n", " ", ""]

    def split_nodes(self, nodes: List[DocumentNode]) -> list[DocumentNode]:
        raise NotImplementedError

    def split_documents(self, documents: Iterable[DocumentNode]) -> list[DocumentNode]:
        print("llamaindex split documents:", documents)
        return []

    def merge_blocks_into_text(cls, blocks: List[Block]) -> str:
        raise NotImplementedError
