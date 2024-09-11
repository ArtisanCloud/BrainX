from typing import List, Tuple, Optional, Any, Sequence

from langchain_postgres.vectorstores import PGVector

from app.core.rag.ingestion.drivers.langchain.helper import convert_nodes_to_documents, convert_documents_to_nodes, \
    convert_document_to_node

from app.core.rag.vector_store.interface import BaseVectorStore
from app.config.agent.pgvector import PGVector as PGVectorConfig
from app.models.rag.document_node import DocumentNode


class PGVectorStore(BaseVectorStore):
    def __init__(
            self,
            config: PGVectorConfig, collection_name: str,
            embedding_model: any
    ):
        """
        初始化 PgVectorStoreDriver 实例。

        :param connection_string: PostgreSQL 数据库连接字符串
        :param table_name: 存储向量的表名
        """

        self.connection_string = config.url
        self.collection_name = collection_name
        self.vector_store = PGVector(
            embeddings=embedding_model,
            connection=self.connection_string,
            collection_name=collection_name,
            use_jsonb=config.use_jsonb,
            # embedding_length=768,
        )

    def add_documents(self, nodes: List[DocumentNode], **kwargs: Any) -> List[str]:
        # convert nodes to documents
        documents = convert_nodes_to_documents(nodes)

        # 实现向量添加功能
        return self.vector_store.add_documents(
            documents,
            ids=[node.metadata["node_id"] for node in nodes],
        )

    def search_by_text(self, text: str, top_k: int, filter_by: dict) -> List[DocumentNode]:
        documents = self.vector_store.similarity_search(text, top_k, filter_by)

        nodes = convert_documents_to_nodes(documents)

        return nodes

    def search_by_vector(self, query_vector: List[float], top_k: int) -> List[DocumentNode]:
        documents = self.vector_store.similarity_search_by_vector(query_vector, top_k)

        nodes = convert_documents_to_nodes(documents)

        return nodes

    def delete_documents(
            self,
            ids: Optional[List[str]] = None,
            collection_only: bool = False,
            **kwargs: Any, ) -> None:
        self.vector_store.delete(ids, collection_only, kwargs=kwargs)

    def update_documents(self, nodes: List[DocumentNode], **kwargs: Any):
        items = convert_nodes_to_documents(nodes)

        response = self.vector_store.upsert(items, kwargs=kwargs)
        if not response:
            raise ValueError("Failed to update vectors")

    def upsert_documents(self, nodes: List[DocumentNode], **kwargs: Any):
        items = convert_nodes_to_documents(nodes)

        response = self.vector_store.upsert(items, kwargs=kwargs)
        if not response:
            raise ValueError("Failed to update vectors")

    def search_with_score(self,
                          query: str,
                          k: int = 4,
                          filter_by: Optional[dict] = None
                          ) -> List[Tuple[DocumentNode, float]]:

        list_documents = self.vector_store.similarity_search_with_score(query, k, filter_by)

        list_nodes: List[Tuple[DocumentNode, float]] = []
        for document, score in list_documents:
            list_nodes.append(
                (convert_document_to_node(document), score)
            )

        return list_nodes
