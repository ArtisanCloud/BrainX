from app.core.rag.vector_store.interface import BaseVectorStore


class LLamaIndexVectorStore(BaseVectorStore):
    

    def __init__(self, vdb_driver: BaseVectorStore) -> None:
        """
        初始化 LLamaIndexVectorStore 实例。

        :param vdb_driver: 实际的向量数据库驱动类（如 FaissVectorStoreDriver 或 PgVectorStoreDriver）
        """
        self.vdb_driver = vdb_driver
        self.driver_instance = None
