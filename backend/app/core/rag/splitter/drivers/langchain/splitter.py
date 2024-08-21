import re
import uuid
from typing import Optional, Any, Iterable, List, Union, Literal

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.libs.node import generate_node_hash
from app.core.rag.splitter.base import BaseTextSplitter
from app.models.rag.document_node import DocumentNode


class LangchainRecursiveCharacterTextSplitter(BaseTextSplitter, RecursiveCharacterTextSplitter):
    def __init__(self, separator: str = "\n\n", separators: Optional[list[str]] = None, **kwargs: Any):
        """Create a new TextSplitter."""
        super().__init__(**kwargs)
        self.separator = separator
        self._separators = separators or ["\n\n", "\n", " ", ""]

    def split_nodes(self, nodes: List[DocumentNode]) -> list[DocumentNode]:
        # 使用langchain的TextSplitter中的 split_documents方法
        # 需要进行类型转换格式
        documents = self.convert_nodes_to_documents(nodes)

        split_documents = self.split_documents(documents)

        split_nodes = self.convert_documents_to_nodes(split_documents)

        return split_nodes

    @classmethod
    def convert_nodes_to_documents(cls, nodes: List[DocumentNode]) -> List[Document]:
        return [
            Document(
                page_content=node.page_content,
                metadata=node.metadata
            )
            for node in nodes
        ]

    @classmethod
    def convert_documents_to_nodes(cls, documents: List[Document]) -> List[DocumentNode]:
        return [
            DocumentNode(
                page_content=document.page_content,
                metadata={
                    **document.metadata,
                    "node_id": str(uuid.uuid4()),
                    "node_hash": generate_node_hash(document.page_content)
                }

            )
            for document in documents
        ]
