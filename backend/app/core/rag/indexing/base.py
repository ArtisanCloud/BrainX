from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from sqlalchemy import UUID

from app.models import DocumentSegment, User, Document
from app.models.rag.document_node import DocumentNode

from enum import Enum


class IndexingDriverType(Enum):
    DEFAULT = "default"
    LANGCHAIN = "langchain"
    LLAMA_INDEX = "llamaindex"

    def __str__(self):
        return self.value


class BaseIndexing(ABC):

    def __init__(self, user: Optional[User] = None, document: Optional[Document] = None):
        self.user = user
        self.document = document

    @abstractmethod
    def transform_documents(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        raise NotImplementedError

    def create_document_segments(self, nodes: List[DocumentNode]) -> List[DocumentSegment]:
        segments = []
        for idx, node in enumerate(nodes):
            segment = DocumentSegment(
                tenant_uuid=UUID(node.tenant_uuid),  # 替换为实际的 tenant_uuid
                document_uuid=UUID(self.document.uuid),  # 替换为实际的 document_uuid
                dataset_uuid=UUID(self.document.dataset_uuid),  # 替换为实际的 dataset_uuid
                created_user_by=UUID(self.user.uuid),  # 替换为实际的 created_user_by
                updated_user_by=None,  # 如果没有更新用户，可以是 None
                status=1,  # 替换为实际的状态
                content=node.page_content,
                position=idx,  # 当前索引
                page_number=self._extract_page_number(node.page_content),  # 从内容中提取页面编号的自定义方法
                word_count=self._count_words(node.page_content),  # 从内容中计算单词数的自定义方法
                token_count=self._count_tokens(node.page_content),  # 从内容中计算 token 数的自定义方法
                keywords=self._extract_keywords(node.page_content),  # 从内容中提取关键词的自定义方法
                hit_count=0,  # 初始值
                index_node_id="some_id",  # 替换为实际的 index_node_id
                index_node_hash="some_hash",  # 替换为实际的 index_node_hash
                error_message=None  # 如果没有错误信息，可以是 None
            )
            segments.append(segment)

        return segments
