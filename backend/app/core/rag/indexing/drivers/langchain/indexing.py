from typing import List, Optional, Tuple

from app import settings
from app.core.ai_model.model_instance import ModelInstance
from app.core.rag import FrameworkDriverType
from app.core.rag.indexing.base import BaseIndexing
from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.core.rag.vector_store.drivers.langchain.vdb import VectorStoreType
from app.core.rag.vector_store.factory import VectorStoreDriverFactory
from app.core.rag.vector_store.interface import BaseVectorStore
from app.models import DocumentSegment, User, Document
from app.models.rag.document_node import DocumentNode


class LangchainIndexer(BaseIndexing):
    """
       Implementation of BaseIndexing for Langchain indexing.
       """

    def __init__(self,
                 user: Optional[User] = None,
                 document: Optional[Document] = None,
                 splitter: Optional[BaseTextSplitter] = None,
                 collection_name: str = "rag_embeddings",
                 embedding_model_instance: Optional[ModelInstance] = None,
                 llm_model_instance: Optional[ModelInstance] = None
                 ):
        super().__init__(user=user, document=document)  # 初始化父类参数
        self.splitter = splitter
        self.embedding_model_instance = embedding_model_instance
        self.llm_model_instance = llm_model_instance
        self.nodes = []

        # get framework driver embedding model from embedding_model_instance
        embedding_model = embedding_model_instance.model.get_provider_model()
        # print("get embedding model:", embedding_model)

        # get vector store
        self.vector_store_driver = VectorStoreDriverFactory.create_vector_store_driver(
            FrameworkDriverType(settings.agent.framework_driver),
            VectorStoreType(settings.agent.vdb),
            collection_name=collection_name,
            embedding_model=embedding_model
        )

        # create retriever
        self.retriever = (
            self.vector_store_driver
            .get_vector_store()
            .get_retriever()
        )

    def transform_documents(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        # 实现存储数据逻辑
        # print("langchain transform segments:", [node.page_content for node in nodes])
        final_nodes: list[DocumentNode] = []
        for node in nodes:
            split_nodes = self.splitter.split_nodes([node])
            # print("split segments:", [node.page_content for node in split_nodes])
            final_nodes.extend(split_nodes)

        return final_nodes

    def get_vector_store(self) -> BaseVectorStore:
        return self.vector_store_driver.get_vector_store()

    def save_nodes_to_store_vector(self, nodes: List[DocumentNode]) -> Tuple[int, int, Optional[Exception]]:
        # print(self.embedding_model_instance, self.llm_model_instance)

        try:
            # 确保embedding_model_instance和vector_store已经初始化
            if not self.embedding_model_instance:
                raise ValueError("Embedding model instance is not initialized.")

            vector_store = self.vector_store_driver.get_vector_store()
            if not vector_store:
                raise ValueError("vector store is not initialized.")

            word_count = 0
            token = 0
            result_list = vector_store.add_documents(nodes)
            # for node, vector in zip(nodes, result_list):
            #     word_count += len(node.page_content.split())

            # 如果一切顺利，返回None表示没有异常
            return word_count, token, None

        except Exception as e:
            # 捕获所有异常并返回
            return 0, 0, e
