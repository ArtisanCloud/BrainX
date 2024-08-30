import uuid
from typing import Optional, Any, List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.libs.node import generate_node_hash
from app.core.rag.indexing.drivers.langchain.helper import convert_nodes_to_documents, convert_documents_to_nodes
from app.core.rag.indexing.splitter.base import BaseTextSplitter
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
        documents = convert_nodes_to_documents(nodes)

        split_documents = self.split_documents(documents)

        split_nodes = convert_documents_to_nodes(split_documents)

        return split_nodes


