from enum import IntEnum

from sqlalchemy import SmallInteger, ForeignKey, Boolean, UUID, Text, Integer, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import BaseModel, table_name_document_segment, table_name_document, table_name_user, \
    table_name_tenant


class DocumentSegmentStatus(IntEnum):
    DRAFT = 1
    FINALIZED = 2
    ARCHIVED = 3
    DELETED = 4
    PENDING = 5
    PROCESSING = 6
    ERROR = 7


class DocumentSegment(BaseModel):
    __tablename__ = table_name_document_segment  # 替换为实际的表名

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    document_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_document + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)

    status = mapped_column(SmallInteger)

    content = mapped_column(Text)
    document_index = mapped_column(Integer)
    word_count = mapped_column(Integer)
    token_count = mapped_column(Integer)

    document: Mapped["Document"] = relationship(back_populates="document_segments", foreign_keys=[document_uuid])

    def __repr__(self):
        content_preview = self.content[:10] + '...' if self.content is not None else 'No content'
        return (
            f"<DocumentSegment(id={self.id}, "
            f"uuid={self.uuid}, "
            f"document_uuid='{self.document_uuid}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"status='{self.status}', "
            f"content='{content_preview}', "
            f"document_index='{self.index}', "
            f"word_count='{self.word_count}', "
            f"token_count='{self.token_count}')>"
        )
