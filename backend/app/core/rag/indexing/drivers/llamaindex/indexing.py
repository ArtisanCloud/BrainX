from typing import List, Optional

from app.core.ai_model.model_instance import ModelInstance
from app.core.rag.indexing.cleaner.base import Cleaner
from app.core.rag.indexing.interface import BaseIndexing
from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.models import User, Document
from app.models.rag.document_node import DocumentNode


class LlamaIndexIndexer(BaseIndexing):
    def __init__(self,
                 user: Optional[User] = None,
                 document: Optional[Document] = None,
                 splitter: BaseTextSplitter = None,
                 embedding_model_instance: Optional[ModelInstance] = None
                 ):
        self.splitter = splitter
        self.embedding_model_instance = embedding_model_instance
        self.nodes = []

    def transform_documents(self, nodes: List[DocumentNode], **kwargs) -> List[DocumentNode]:
        # 实现存储数据逻辑
        # print("llamaindex transform segments:", [node.page_content for node in nodes])
        final_documents = []
        for node in nodes:
            # clean document
            document_text = Cleaner.clean(node.page_content, kwargs.get('process_rule'))
            node.page_content = document_text

            # parse document to nodes
            document_nodes = self.split_documents([node])

        # print("split segments:", [segment.page_content for segment in segments])

        return []
