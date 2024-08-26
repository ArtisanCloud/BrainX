from typing import List, Optional

from app.core.ai_model.model_instance import ModelInstance
from app.core.rag.indexing.base import BaseIndexing
from app.core.rag.indexing.splitter.base import BaseTextSplitter
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
                 embedding_model_instance: Optional[ModelInstance] = None
                 ):
        super().__init__(user=user, document=document)  # 初始化父类参数
        self.splitter = splitter
        self.embedding_model_instance = embedding_model_instance
        self.nodes = []

        self.vector_store = settings.

    def transform_documents(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        # 实现存储数据逻辑
        # print("langchain transform segments:", [node.page_content for node in nodes])
        final_nodes: list[DocumentNode] = []
        for node in nodes:
            split_nodes = self.splitter.split_nodes([node])
            # print("split segments:", [node.page_content for node in split_nodes])
            final_nodes.extend(split_nodes)

        return final_nodes

    def save_nodes_to_store_vector(self, nodes: List[DocumentNode]) -> Optional[Exception]:

        return None
