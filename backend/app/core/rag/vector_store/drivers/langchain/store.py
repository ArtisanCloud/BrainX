from abc import abstractmethod
from typing import List, Optional, Tuple, Dict, Type, Any

from app.core.rag.retrieval.interface import BaseRetriever
from app.core.rag.vector_store.interface import VectorStoreDriver, BaseVectorStore
from app.models.rag.document_node import DocumentNode


class LangchainVectorStoreDriver(VectorStoreDriver):
    def __init__(self, vector_store: BaseVectorStore) -> None:
        """
        初始化 LangchainVectorStore 实例。

        :param vdb_driver: 实际的向量数据库驱动类（如 FaissVectorStore 或 PgVectorStoreDriver）
        """
        self.vector_store = vector_store

    def get_base_vector_store(self) -> BaseVectorStore:
        return self.vector_store

