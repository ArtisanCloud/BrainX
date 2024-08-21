from typing import List, Tuple, Dict, Optional
from langchain_postgres.vectorstores import PGVector  # 从 langchain_postgres 导入 PostgreSQL 向量存储接口

from app.core.rag.vector_store.interface import BaseVectorStore


class PGVectorStoreDriver(BaseVectorStore):
    def __init__(self, connection_string: str, table_name: str):
        """
        初始化 PgVectorStoreDriver 实例。

        :param connection_string: PostgreSQL 数据库连接字符串
        :param table_name: 存储向量的表名
        """
        self.connection_string = connection_string
        self.table_name = table_name
        self.store = PGVector(connection_string, table_name)

    def add_vectors(self, vectors: List[List[float]], document_ids: List[str],
                    metadata: Optional[List[Dict]] = None) -> None:
        """
        将向量添加到 PostgreSQL 向量存储中。

        :param vectors: 向量列表
        :param document_ids: 文档 ID 列表
        :param metadata: 元数据列表（可选）
        """
        # 实现向量添加功能
        self.store.add(vectors, document_ids, metadata)

    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[str, float]]:
        """
        根据查询向量在 PostgreSQL 向量存储中进行搜索。

        :param query_vector: 查询向量
        :param top_k: 返回最相似的K个向量
        :return: 文档 ID 和相似度得分的列表
        """
        # 实现搜索功能
        return self.store.search(query_vector, top_k)

    def delete_vectors(self, document_ids: List[str]) -> None:
        """
        删除与指定文档 ID 相关联的向量。

        :param document_ids: 要删除的文档 ID 列表
        """
        # 实现删除功能
        self.store.delete(document_ids)

    def update_vector(self, vector: List[float], document_id: str, metadata: Optional[Dict] = None) -> None:
        """
        更新与指定文档 ID 相关联的向量及其元数据。

        :param vector: 要更新的向量
        :param document_id: 要更新的文档 ID
        :param metadata: 要更新的元数据（可选）
        """
        # 实现更新功能
        self.store.update(vector, document_id, metadata)

    def get_vector(self, document_id: str) -> Tuple[List[float], Optional[Dict]]:
        """
        根据文档 ID 获取向量及其元数据。

        :param document_id: 要检索的文档 ID
        :return: 向量及元数据
        """
        # 实现检索功能
        vector, metadata = self.store.get(document_id)
        return vector, metadata

    def batch_search_vectors(self, query_vectors: List[List[float]], top_k: int) -> List[List[Tuple[str, float]]]:
        """
        批量搜索查询向量。

        :param query_vectors: 批量查询向量
        :param top_k: 每个查询向量返回最相似的K个向量
        :return: 每个查询向量的文档 ID 和相似度得分的列表
        """
        # 实现批量搜索功能
        return [self.store.search(query_vector, top_k) for query_vector in query_vectors]
