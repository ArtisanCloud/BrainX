from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any

from app.models.rag.document_node import DocumentNode


class BaseVectorStore(ABC):

    def __init__(self):
        self.vector_store = None

    def get_vector_store(self) -> any:
        return self.vector_store

    @abstractmethod
    def add_documents(self, nodes: List[DocumentNode], **kwargs: Any) -> List[str]:
        """
        添加多个文档到向量存储中，并返回每个文档的唯一标识符列表。

        参数:
        - documents (List[DocumentNode]): 需要存储的文档列表。每个文档可以是文本、向量或其他数据类型，具体取决于实现。
        - **kwargs (Any): 其他可选参数，用于配置或调整存储行为。具体参数根据实现不同可能有所变化。

        返回:
        - List[str]: 每个文档的唯一标识符列表，用于后续检索或管理。
        """
        pass

    @abstractmethod
    def search_by_text(self, text: str, top_k: int, filter_by: dict) -> List[DocumentNode]:
        pass

    @abstractmethod
    def search_by_vector(self, query_vector: List[float], top_k: int) -> List[DocumentNode]:
        pass

    @abstractmethod
    def delete_documents(self, document_ids: List[str], collection_only: bool = False, ) -> None:
        pass

    @abstractmethod
    def update_documents(self, nodes: List[DocumentNode], **kwargs: Any):
        pass

    def upsert_documents(self, nodes: List[DocumentNode], **kwargs: Any):
        pass

    @abstractmethod
    def search_with_score(self,
                          query: str,
                          k: int = 4,
                          filter_by: Optional[dict] = None
                          ) -> List[Tuple[DocumentNode, float]]:
        pass


class VectorStoreDriver(ABC):
    @abstractmethod
    def get_base_vector_store(self) -> "BaseVectorStore":
        raise NotImplementedError
