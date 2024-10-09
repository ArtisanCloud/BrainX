from enum import IntEnum

from sqlalchemy import String, SmallInteger, ForeignKey, JSON, UUID, Text, Integer, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import settings
from app.models.base import BaseORM, table_name_document_segment, table_name_document, table_name_user, \
    table_name_tenant, table_name_dataset
from app.models.rag.document_node import DocumentNode


class DocumentSegmentStatus(IntEnum):
    DRAFT = 1
    FINALIZED = 2
    ARCHIVED = 3
    DELETED = 4
    PENDING = 5
    PROCESSING = 6
    ERROR = 7


class DocumentSegment(BaseORM):
    __tablename__ = table_name_document_segment  # 替换为实际的表名
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'), index=True)
    document_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_document + '.uuid'), index=True)
    dataset_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_dataset + '.uuid'), index=True)
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False,
                                    index=True)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True,
                                    index=True)

    status = mapped_column(SmallInteger)
    content = mapped_column(Text)
    position = mapped_column(Integer)
    page_number = mapped_column(Integer)
    word_count = mapped_column(Integer)
    token_count = mapped_column(Integer)

    keywords = mapped_column(JSON)
    hit_count = mapped_column(Integer)
    index_node_id = mapped_column(String, index=True)
    index_node_hash = mapped_column(String, index=True)
    error_message = mapped_column(Text)

    document: Mapped["Document"] = relationship(back_populates="document_segments", foreign_keys=[document_uuid])

    nodes: list[DocumentNode] = []

    def __repr__(self):
        content_preview = self.content[:10] + '...' if self.content is not None else 'No content'
        return (
            f"<DocumentSegment("
            # f"id={self.id}, "
            f"uuid={self.uuid}, "
            f"document_uuid='{self.document_uuid}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"status='{self.status}', "
            f"content='{content_preview}', "
            f"position='{self.position}', "
            f"word_count='{self.word_count}', "
            f"token_count='{self.token_count}')>"
        )
