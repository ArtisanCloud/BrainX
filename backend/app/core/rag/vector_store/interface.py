from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict


class BaseVectorStore(ABC):
    @abstractmethod
    def add_vectors(self, vectors: List[List[float]], document_ids: List[str],
                    metadata: Optional[List[Dict]] = None) -> None:
        """
        添加一组向量到存储中，与每个向量相关联的文档ID一起保存。

        :param vectors: 要添加的向量列表
        :param document_ids: 与每个向量相关联的文档ID列表
        :param metadata: 选填，相关联的元数据列表
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
