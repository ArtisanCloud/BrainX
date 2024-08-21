from enum import IntEnum
from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, UUID, Text, Integer, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import BaseORM, table_name_document, table_name_dataset, table_name_user, table_name_tenant, \
    table_name_media_resource
from app.schemas.base import BaseSchema


class DocumentType(IntEnum):
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4


class DocumentStatus(IntEnum):
    DRAFT = 1
    PUBLISHED = 2
    ARCHIVED = 3


class Document(BaseORM):
    __tablename__ = table_name_document  # 替换为实际的表名

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    dataset_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_dataset + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)
    resource_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_media_resource + '.uuid'), nullable=True)

    title = mapped_column(String)
    # resource_type = mapped_column(SmallInteger)
    resource_url = mapped_column(String)
    status = mapped_column(SmallInteger)
    type = mapped_column(SmallInteger)
    document_index = mapped_column(Integer)
    batch_index = mapped_column(Integer)
    word_count = mapped_column(Integer)
    token_count = mapped_column(Integer)

    process_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    process_end_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    parse_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    parse_end_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    split_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    split_end_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    dataset: Mapped["Dataset"] = relationship(back_populates="documents", foreign_keys=[dataset_uuid])
    document_segments: Mapped["DocumentSegment"] = relationship(back_populates="document",
                                                                foreign_keys="[DocumentSegment.document_uuid]")

    # tenant: Mapped["Tenat"] = relationship(back_populates="datasets", foreign_keys=[tenant_uuid])
    # created_user_by: Mapped["User"] = relationship(back_populates="created_documents", foreign_keys=[created_user_by])
    # updated_user_by: Mapped["User"] = relationship(back_populates="updated_documents", foreign_keys=[updated_user_by])

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "tenant_uuid": str(self.tenant_uuid),
            "dataset_uuid": str(self.dataset_uuid),
            "created_user_by": str(self.created_user_by),
            "updated_user_by": str(self.updated_user_by) if self.updated_user_by else None,
            "resource_uuid": str(self.resource_uuid) if self.resource_uuid else None,
            "title": self.title,
            "status": self.status,
            "type": self.type,
            "document_index": self.document_index,
            "batch_index": self.batch_index,
            "word_count": self.word_count,
            "token_count": self.token_count,
            "resource_url": self.resource_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def __repr__(self):
        return (
            f"<Document(id={self.id}, "
            f"uuid={self.uuid}, "
            f"dataset_uuid='{self.dataset_uuid}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"resource_uuid='{self.resource_uuid}', "
            f"title='{self.title}', "
            f"status='{self.status}', "
            f"type='{self.type}', "
            f"document_index='{self.document_index}', "
            f"batch_index='{self.batch_index}', "
            f"word_count='{self.word_count}', "
            f"token_count='{self.token_count}', "
            f"resource_url='{self.resource_url}', "
            f"process_start_at='{self.process_start_at}', "
            f"process_end_at='{self.process_end_at}', "
            f"parse_start_at='{self.parse_start_at}', "
            f"parse_end_at='{self.parse_end_at}', "
            f"split_start_at='{self.split_start_at}', "
            f"split_end_at='{self.split_end_at}')>"
        )
