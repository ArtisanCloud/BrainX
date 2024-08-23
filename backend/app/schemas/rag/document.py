from typing import Optional, List

from pydantic import constr, Field

from app.models.rag.document import Document
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema
from app.schemas.media_resource.schema import MediaResourceSchema
from app.schemas.rag.document_segment import DocumentSegmentSchema
from app.service.rag.document_segment.list import transform_document_segments_to_reply


class DocumentSchema(BaseObjectSchema):
    dataset_uuid: Optional[str] = None  # UUID应该是字符串类型，这里正确
    tenant_uuid: Optional[str] = None  # UUID应该是字符串类型，这里正确
    data_source_type: Optional[int] = None  # 数据源类型应该是整数类型，这里应该为int
    resource_uuid: Optional[str] = None  # UUID应该是字符串类型，这里正确
    resource_url: Optional[str] = None  # URL应该是字符串类型，这里正确
    status: Optional[int] = None  # 状态通常表示为整数，这里正确
    type: Optional[int] = None  # 类型通常表示为整数，这里正确
    batch: Optional[str] = None  # 批次应该是字符串类型，因为它通常是一个标识符或名称
    dataset_process_rule_uuid: Optional[str] = None  # UUID应该是字符串类型，这里应改为str
    created_source: Optional[str] = None  # 创建来源通常是字符串（如 'web'），应改为str
    created_user_by: Optional[str] = None  # UUID应该是字符串类型，这里应改为str
    updated_user_by: Optional[str] = None  # UUID应该是字符串类型，这里正确
    indexing_status: Optional[int] = None  # 索引状态通常表示为整数，这里应改为int
    process_start_at: Optional[str] = None  # 开始时间应为str类型
    process_end_at: Optional[str] = None  # 结束时间应为str类型
    word_count: Optional[int] = None  # 词数应为整数类型
    parse_start_at: Optional[str] = None  # 解析开始时间应为str类型
    clean_start_at: Optional[str] = None  # 清理开始时间应为str类型
    split_start_at: Optional[str] = None  # 分割开始时间应为str类型
    token_count: Optional[int] = None  # 令牌计数应为整数类型
    indexing_latency: Optional[float] = None  # 索引延迟应为浮点数
    is_paused: Optional[bool] = None  # 是否暂停应为布尔类型
    paused_by: Optional[str] = None  # UUID应该是字符串类型，这里正确
    paused_at: Optional[str] = None  # 暂停时间应为str类型
    error_message: Optional[str] = None  # 错误消息应为字符串类型
    error_at: Optional[str] = None  # 错误发生时间应为str类型
    is_archived: Optional[bool] = None  # 是否归档应为布尔类型
    archived_reason: Optional[str] = None  # 归档原因应为字符串类型
    archived_by: Optional[str] = None  # UUID应该是字符串类型，这里正确
    archived_at: Optional[str] = None  # 归档时间应为str类型
    title: Optional[str] = None  # 标题应为字符串类型
    document_type: Optional[str] = None  # 文档类型应为字符串类型
    document_meta: Optional[dict] = None  # 文档元数据应为字典类型
    document_index: Optional[int] = None  # 文档索引应为整数类型

    document_segments: List[DocumentSegmentSchema] = Field(default_factory=list)

    @classmethod
    def from_orm(cls, obj: Document):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            dataset_uuid=str(obj.dataset_uuid),
            tenant_uuid=str(obj.tenant_uuid),
            data_source_type=obj.data_source_type,
            resource_uuid=str(obj.resource_uuid),
            resource_url=obj.resource_url,
            status=obj.status,
            type=obj.type,
            batch=obj.batch,
            dataset_process_rule_uuid=str(obj.dataset_process_rule_uuid),
            created_source=obj.created_source,
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            indexing_status=obj.indexing_status,
            process_start_at=obj.process_start_at,
            process_end_at=obj.process_end_at,
            word_count=obj.word_count,
            parse_start_at=obj.parse_start_at,
            clean_start_at=obj.clean_start_at,
            split_start_at=obj.split_start_at,
            token_count=obj.token_count,
            indexing_latency=obj.indexing_latency,
            is_paused=obj.is_paused,
            paused_by=str(obj.paused_by) if obj.paused_by else None,
            paused_at=obj.paused_at,
            error_message=obj.error_message,
            error_at=obj.error_at,
            is_archived=obj.is_archived,
            archived_reason=obj.archived_reason,
            archived_by=str(obj.archived_by) if obj.archived_by else None,
            archived_at=obj.archived_at,
            title=obj.title,
            document_type=obj.document_type,
            document_meta=obj.document_meta,
            document_index=obj.document_index,

            # document_segments=transform_document_segments_to_reply(obj.document_segments)
        )


class RequestGetDocumentList(BaseSchema):
    pagination: Optional[Pagination] = None


class ResponseGetDocumentList(BaseSchema):
    data: list[DocumentSchema]
    pagination: ResponsePagination


class ResponseGetDocument(BaseSchema):
    data: DocumentSchema


class RequestCreateDocument(DocumentSchema):
    content: constr(min_length=1)


class ResponseCreateDocument(BaseSchema):
    document: DocumentSchema


class RequestPatchDocument(DocumentSchema):
    pass


class ResponsePatchDocument(BaseSchema):
    document: DocumentSchema


class ResponseDeleteDocument(BaseSchema):
    result: bool


class SegmentationRuleSchema(BaseSchema):
    segment_id: str
    max_chunk_length: int
    overlap_chunk_length: int


class RuleSchema(BaseSchema):
    segmentation: SegmentationRuleSchema


class RequestAddDocumentContent(DocumentSchema):
    dataset_uuid: str
    media_resources: List[MediaResourceSchema]
    rule_mode: Optional[int] = None
    rule: Optional[RuleSchema] = None


class ResponseAddDocumentContent(BaseSchema):
    data: list[DocumentSchema]
    task_ids: List[str]


class RequestReProcessDocuments(DocumentSchema):
    document_uuids: List[str]


class RequestReProcessDocument(DocumentSchema):
    document_uuid: str


class ResponseReProcessDocuments(BaseSchema):
    task_ids: List[str]


def make_document(document: DocumentSchema) -> Document:
    return Document(
        tenant_uuid=document.tenant_uuid,
        dataset_uuid=document.dataset_uuid,
        created_user_by=document.created_user_by,
        updated_user_by=document.updated_user_by,
        title=document.title,
        status=document.status,
        type=document.type,
        document_index=document.document_index,
        batch_index=document.batch_index,
        word_count=document.word_count,
        token_count=document.token_count,
        overlap_size=document.overlap_size,
        process_start_at=document.process_start_at,
        process_end_at=document.process_end_at,
        parse_start_at=document.parse_start_at,
        parse_end_at=document.parse_end_at,
        split_start_at=document.split_start_at,
        split_end_at=document.split_end_at,

    )
