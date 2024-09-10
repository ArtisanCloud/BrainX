from app.core.rag.vector_store.interface import BaseVectorStore, VectorStoreDriver


class LlamaIndexVectorStoreDriver(VectorStoreDriver):

    def __init__(self, vector_store: BaseVectorStore) -> None:
        """
        初始化 LlamaIndexVectorStore 实例。

        :param vdb_driver: 实际的向量数据库驱动类（如 FaissVectorStore 或 PgVectorStoreDriver）
        """
        self.vector_store = vector_store

    def get_vector_store(self):
        return self.vector_store

