from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any

from app.models.rag.document_node import DocumentNode


class VectorStoreDriver(ABC):
    @abstractmethod
    def get_vector_store(self):
        raise NotImplementedError

class BaseVectorStore(ABC):
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
    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[str, float]]:
        """
        根据查询向量搜索最相似的向量，并返回相关联的文档ID及相似度。

        :param query_vector: 用于搜索的查询向量
        :param top_k: 返回最相似的K个向量
        :return: 包含文档ID和相似度得分的列表
        """
        pass

    @abstractmethod
    def delete_vectors(self, document_ids: List[str]) -> None:
        """
        删除与指定文档ID相关联的向量。

        :param document_ids: 要删除的文档ID列表
        """
        pass

    @abstractmethod
    def update_vector(self, vector: List[float], document_id: str, metadata: Optional[Dict] = None) -> None:
        """
        更新与指定文档ID相关联的向量及其元数据。

        :param vector: 要更新的向量
        :param document_id: 要更新的文档ID
        :param metadata: 选填，要更新的元数据
        """
        pass

    @abstractmethod
    def get_vector(self, document_id: str) -> Tuple[List[float], Optional[Dict]]:
        """
        根据文档ID获取相关联的向量及其元数据。

        :param document_id: 要检索的文档ID
        :return: 返回与文档ID相关联的向量及元数据
        """
        pass

    @abstractmethod
    def batch_search_vectors(self, query_vectors: List[List[float]], top_k: int) -> List[List[Tuple[str, float]]]:
        """
        批量搜索查询向量，返回每个查询向量最相似的文档ID及相似度得分。

        :param query_vectors: 批量查询向量
        :param top_k: 每个查询向量返回最相似的K个向量
        :return: 每个查询返回的文档ID和相似度得分的列表
        """
        pass
