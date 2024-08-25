from enum import IntEnum

from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, UUID, Text, Integer, TIMESTAMP, Float, JSON
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import BaseORM, table_name_document, table_name_dataset, table_name_user, table_name_tenant, \
    table_name_media_resource, table_name_dataset_segment_rule


class DocumentType(IntEnum):
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4


class DataSourceType(IntEnum):
    Upload_FILE = 1
    CRAWLER_URL = 2
    IMPORT_PLATFORM = 3


class ContentType(IntEnum):
    LOCAL_DOCUMENT = 1
    ONLINE_DATA = 2
    NOTION = 3
    GOOGLE_DOC = 4
    LARK = 5
    CUSTOM = 6

    @classmethod
    def get_content_type_names(cls):
        return list(cls.__members__.keys())


class DocumentStatus(IntEnum):
    DRAFT = 0  # 文档初始状态，可能尚未提交处理
    NORMAL = 1  # 文档正常状态


class DocumentIndexingStatus(IntEnum):
    PENDING = 1  # 文档已提交，等待开始处理
    PARSING = 2  # 正在解析加载文档内容
    EXTRACTING = 3  # 正在提取文档的关键部分或内容（如提取文本片段）
    CLEANING = 4  # 正在清理或预处理提取的内容（如去邮件，url，或者记录清理等）
    SPLITTING = 5  # 正在进行主要处理分段步骤（如splitter）
    INDEXING = 6  # 正在进行拆分内容向量化处理
    COMPLETED = 7  # 文档处理完成，所有步骤成功
    ARCHIVED = 8  # 文档已归档，可能不再进行处理
    PAUSE = 9  # 处理过程中暂停了
    ERROR = 10  # 处理过程中出现错误


class Document(BaseORM):
    __tablename__ = table_name_document  # 替换为实际的表名

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    dataset_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_dataset + '.uuid'))

    # resource info
    data_source_type = mapped_column(SmallInteger)
    resource_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_media_resource + '.uuid'), nullable=True)
    resource_url = mapped_column(String)

    # Document metadata
    status = mapped_column(SmallInteger)
    type = mapped_column(SmallInteger)
    content_type = mapped_column(SmallInteger)

    # Batch and process rule
    batch = mapped_column(String)
    dataset_process_rule_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_dataset_segment_rule + '.uuid'),
                                              nullable=True)

    # Created and updated info
    created_source = mapped_column(String)
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)

    # step flow
    indexing_status = mapped_column(SmallInteger)
    process_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    process_end_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # step parsing
    word_count = mapped_column(Integer)
    parse_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # step cleaning
    clean_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # step splitting
    split_start_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # step indexing with embedding and vector store
    token_count = mapped_column(Integer)
    indexing_latency = mapped_column(Float)

    # pause
    is_paused = mapped_column(Boolean, default=False)
    paused_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)
    paused_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # error
    error_message = mapped_column(String)
    error_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # archive
    is_archived = mapped_column(Boolean, nullable=True)
    archived_reason = mapped_column(String, nullable=True)
    archived_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)
    archived_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    # document info
    title = mapped_column(String)
    document_type = mapped_column(String(50), nullable=True)
    document_meta = mapped_column(JSON, nullable=True)
    document_index = mapped_column(Integer, nullable=True)

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
            "data_source_type": self.data_source_type,
            "resource_uuid": str(self.resource_uuid) if self.resource_uuid else None,
            "resource_url": self.resource_url,
            "status": self.status,
            "type": self.type,
            "content_type": self.content_type,
            "batch": self.batch,
            "dataset_process_rule_uuid": str(
                self.dataset_process_rule_uuid) if self.dataset_process_rule_uuid else None,
            "created_source": self.created_source,
            "created_user_by": str(self.created_user_by),
            "updated_user_by": str(self.updated_user_by) if self.updated_user_by else None,
            "indexing_status": self.indexing_status,
            "process_start_at": self.process_start_at,
            "process_end_at": self.process_end_at,
            "word_count": self.word_count,
            "parse_start_at": self.parse_start_at,
            "clean_start_at": self.clean_start_at,
            "split_start_at": self.split_start_at,
            "token_count": self.token_count,
            "indexing_latency": self.indexing_latency,
            "is_paused": self.is_paused,
            "paused_by": str(self.paused_by) if self.paused_by else None,
            "paused_at": self.paused_at,
            "error_message": self.error_message,
            "error_at": self.error_at,
            "is_archived": self.is_archived,
            "archived_reason": self.archived_reason,
            "archived_by": str(self.archived_by) if self.archived_by else None,
            "archived_at": self.archived_at,
            "title": self.title,
            "document_type": self.document_type,
            "document_meta": self.document_meta,
            "document_index": self.document_index,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

    def __repr__(self):
        return (
            f"<Document("
            # f"id={self.id}, "
            f"dataset_uuid={self.dataset_uuid}, "
            f"data_source_type={self.data_source_type}, "
            f"resource_uuid={self.resource_uuid}, "
            f"resource_url='{self.resource_url}', "
            f"status={self.status}, type={self.type}, "
            f"content_type={self.content_type}, "
            f"batch='{self.batch}', "
            f"dataset_process_rule_uuid={self.dataset_process_rule_uuid}, "
            f"created_source='{self.created_source}', "
            f"created_user_by={self.created_user_by}, "
            f"updated_user_by={self.updated_user_by}, "
            f"indexing_status={self.indexing_status}, "
            f"process_start_at={self.process_start_at}, "
            f"process_end_at={self.process_end_at}, "
            f"word_count={self.word_count}, "
            f"parse_start_at={self.parse_start_at}, "
            f"clean_start_at={self.clean_start_at}, "
            f"split_start_at={self.split_start_at}, "
            f"token_count={self.token_count}, "
            f"indexing_latency={self.indexing_latency},"
            f" is_paused={self.is_paused}, "
            f"paused_by={self.paused_by}, "
            f"paused_at={self.paused_at}, "
            f"error_message='{self.error_message}', "
            f"error_at={self.error_at}, "
            f"is_archived={self.is_archived}, "
            f"archived_reason='{self.archived_reason}', "
            f"archived_by={self.archived_by}, "
            f"archived_at={self.archived_at}, "
            f"title='{self.title}', "
            f"document_type='{self.document_type}', "
            f"document_meta={self.document_meta}, "
            f"document_index={self.document_index}"
            f")> "

        )
