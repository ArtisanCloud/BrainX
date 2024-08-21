from typing import List

from app.core.rag.cleaner.base import Cleaner
from app.core.rag.indexing.interface import BaseIndexing
from app.core.rag.splitter.base import BaseTextSplitter
from app.models.rag.document_node import DocumentNode


class LLamaIndexIndexer(BaseIndexing):
    def __init__(self, splitter: BaseTextSplitter = None):
        self.splitter = splitter

    def transform_documents(self, documents: List[DocumentNode], **kwargs) -> List[DocumentNode]:
        # 实现存储数据逻辑
        # print("llamaindex transform segments:", [node.page_content for node in nodes])
        final_documents = []
        for document in documents:
            # clean document
            document_text = Cleaner.clean(document.page_content, kwargs.get('process_rule'))
            document.page_content = document_text

            # parse document to nodes
            document_nodes = self.split_documents([document])

        # print("split segments:", [segment.page_content for segment in segments])

        return []
