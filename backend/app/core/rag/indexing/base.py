from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from app.core.rag.vector_store.interface import BaseVectorStore
from app.models import DocumentSegment, User, Document
from app.models.rag.document import DocumentStatus
from app.models.rag.document_node import DocumentNode


class BaseIndexing(ABC):

    def __init__(self, user: Optional[User] = None, document: Optional[Document] = None):
        self.user = user
        self.document = document

    @abstractmethod
    def transform_documents(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        raise NotImplementedError

    @abstractmethod
    def save_nodes_to_store_vector(self, nodes: List[DocumentNode]) -> Tuple[int, int, Exception]:
        raise NotImplementedError

    @abstractmethod
    def get_vector_store(self) -> BaseVectorStore:
        raise NotImplementedError

    def create_document_segments(self, nodes: List[DocumentNode]) -> List[DocumentSegment]:
        segments = []
        for idx, node in enumerate(nodes):
            segment = DocumentSegment(
                tenant_uuid=self.document.tenant_uuid,
                document_uuid=self.document.uuid,
                dataset_uuid=self.document.dataset_uuid,
                created_user_by=self.user.uuid,
                updated_user_by=None,  # 如果没有更新用户，可以是 None
                status=DocumentStatus.NORMAL,
                content=node.page_content,
                position=idx,  # 当前索引
                page_number=node.metadata.get("page_content"),  # 从内容中提取页面编号的自定义方法
                word_count=len(node.page_content),  # 从内容中计算单词数的自定义方法
                token_count=0,  # 从内容中计算 token 数的自定义方法
                keywords="",  # 从内容中提取关键词的自定义方法
                hit_count=0,  # 初始值
                index_node_id=node.metadata.get("index_node_id", ""),
                index_node_hash=node.metadata.get("index_node_hash", ""),
                error_message=None  # 如果没有错误信息，可以是 None
            )
            segments.append(segment)

        return segments
