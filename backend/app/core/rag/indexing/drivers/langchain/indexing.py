from typing import List

from app.core.rag.indexing.interface import BaseIndexing
from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.models.rag.document_node import DocumentNode


class LangchainIndexer(BaseIndexing):
    """
       Implementation of BaseIndexing for Langchain indexing.
       """

    def __init__(self, splitter: BaseTextSplitter = None):
        self.splitter = splitter

    def transform_documents(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        # 实现存储数据逻辑
        # print("langchain transform segments:", [node.page_content for node in nodes])
        final_nodes: list[DocumentNode] = []
        for node in nodes:
            split_nodes = self.splitter.split_nodes([node])
            # print("split segments:", [node.page_content for node in split_nodes])
            final_nodes.extend(split_nodes)

        return final_nodes
