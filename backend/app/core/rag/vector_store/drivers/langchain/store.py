from typing import List, Optional, Tuple, Dict, Type

from app.core.rag.vector_store.interface import BaseVectorStore


class LangchainVectorStore(BaseVectorStore):
    def __init__(self, vdb_driver: BaseVectorStore) -> None:
        """
        初始化 LangchainVectorStore 实例。

        :param vdb_driver: 实际的向量数据库驱动类（如 FaissVectorStoreDriver 或 PgVectorStoreDriver）
        """
        self.vdb_driver = vdb_driver
        self.driver_instance = None

    def _initialize_driver(self, *args, **kwargs) -> None:
        """
        初始化实际的向量数据库驱动实例。
        """
        if not self.driver_instance:
            self.driver_instance = self.vdb_driver(*args, **kwargs)

    def add_vectors(self, vectors: List[List[float]], document_ids: List[str],
                    metadata: Optional[List[Dict]] = None) -> None:
        """
        添加向量到存储中。

        :param vectors: 向量列表
        :param document_ids: 文档ID列表
        :param metadata: 元数据列表
        """
        self._initialize_driver()
        self.driver_instance.add_vectors(vectors, document_ids, metadata)

    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[str, float]]:
        """
        根据查询向量进行搜索。

        :param query_vector: 查询向量
        :param top_k: 返回最相似的K个向量
        :return: 文档ID和相似度的列表
        """
        self._initialize_driver()
        return self.driver_instance.search_vectors(query_vector, top_k)

    def delete_vectors(self, document_ids: List[str]) -> None:
        """
        删除与指定文档ID相关联的向量。

        :param document_ids: 要删除的文档ID列表
        """
        self._initialize_driver()
        self.driver_instance.delete_vectors(document_ids)

    def update_vector(self, vector: List[float], document_id: str, metadata: Optional[Dict] = None) -> None:
        """
        更新与指定文档ID相关联的向量及其元数据。

        :param vector: 向量
        :param document_id: 文档ID
        :param metadata: 元数据
        """
        self._initialize_driver()
        self.driver_instance.update_vector(vector, document_id, metadata)

    def get_vector(self, document_id: str) -> Tuple[List[float], Optional[Dict]]:
        """
        根据文档ID获取向量及元数据。

        :param document_id: 文档ID
        :return: 向量及元数据
        """
        self._initialize_driver()
        return self.driver_instance.get_vector(document_id)

    def batch_search_vectors(self, query_vectors: List[List[float]], top_k: int) -> List[List[Tuple[str, float]]]:
        """
        批量搜索查询向量。

        :param query_vectors: 批量查询向量
        :param top_k: 每个查询向量返回最相似的K个向量
        :return: 每个查询的文档ID和相似度的列表
        """
        self._initialize_driver()
        return self.driver_instance.batch_search_vectors(query_vectors, top_k)
