from typing import List, Tuple, Dict, Optional
import faiss
import numpy as np

from app.core.rag.vector_store.interface import BaseVectorStore


class FaissVectorStoreDriver(BaseVectorStore):
    def __init__(self, dimension: int, index_path: Optional[str] = None):
        """
        初始化 FaissVectorStoreDriver 实例。

        :param dimension: 向量的维度
        :param index_path: 索引文件的路径（如果存在）
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离进行索引

        if index_path:
            self.index = faiss.read_index(index_path)

    def add_vectors(self, vectors: List[List[float]], document_ids: List[str],
                    metadata: Optional[List[Dict]] = None) -> None:
        """
        将向量添加到 FAISS 向量存储中。

        :param vectors: 向量列表
        :param document_ids: 文档 ID 列表
        :param metadata: 元数据列表（可选）
        """
        # 转换为 numpy 数组
        vectors_np = np.array(vectors).astype('float32')
        self.index.add(vectors_np)

        # 这里省略了元数据的存储和更新，可以通过其他机制实现

    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[str, float]]:
        """
        根据查询向量在 FAISS 向量存储中进行搜索。

        :param query_vector: 查询向量
        :param top_k: 返回最相似的K个向量
        :return: 文档 ID 和相似度得分的列表
        """
        # 转换为 numpy 数组
        query_vector_np = np.array(query_vector).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_vector_np, top_k)

        # 将搜索结果转换为 (document_id, distance) 元组的列表
        # 这里的 document_ids 需要与添加时的顺序一致
        return [(str(idx), float(dist)) for idx, dist in zip(indices[0], distances[0])]

    def delete_vectors(self, document_ids: List[str]) -> None:
        """
        删除与指定文档 ID 相关联的向量。
        FAISS 不支持直接删除向量的操作。通常需要重建索引来完成删除操作。
        """
        # 需要实现向量删除的替代方案，比如重新创建索引
        raise NotImplementedError("FAISS does not support direct deletion of vectors.")

    def update_vector(self, vector: List[float], document_id: str, metadata: Optional[Dict] = None) -> None:
        """
        更新与指定文档 ID 相关联的向量及其元数据。
        FAISS 不支持直接更新向量的操作。通常需要重建索引来完成更新操作。
        """
        # 需要实现向量更新的替代方案，比如重新创建索引
        raise NotImplementedError("FAISS does not support direct updating of vectors.")

    def get_vector(self, document_id: str) -> Tuple[List[float], Optional[Dict]]:
        """
        根据文档 ID 获取向量及其元数据。
        FAISS 不支持直接通过文档 ID 获取向量的操作。
        """
        # 需要实现向量检索的替代方案，比如从其他存储中检索
        raise NotImplementedError("FAISS does not support retrieving vectors by document ID.")

    def batch_search_vectors(self, query_vectors: List[List[float]], top_k: int) -> List[List[Tuple[str, float]]]:
        """
        批量搜索查询向量。

        :param query_vectors: 批量查询向量
        :param top_k: 每个查询向量返回最相似的K个向量
        :return: 每个查询向量的文档 ID 和相似度得分的列表
        """
        query_vectors_np = np.array(query_vectors).astype('float32')
        distances, indices = self.index.search(query_vectors_np, top_k)

        return [
            [(str(idx), float(dist)) for idx, dist in zip(indices[i], distances[i])]
            for i in range(len(query_vectors))
        ]
