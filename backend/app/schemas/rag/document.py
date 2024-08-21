from typing import Optional, List

from pydantic import constr, Field

from app.models.rag.document import Document
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema
from app.schemas.media_resource.schema import MediaResourceSchema
from app.schemas.rag.document_segment import DocumentSegmentSchema
from app.service.rag.document_segment.list import transform_document_segments_to_reply


class DocumentSchema(BaseObjectSchema):
    title: Optional[str] = None
    dataset_uuid: Optional[str] = None
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    status: Optional[int] = None
    type: Optional[int] = None
    document_index: Optional[int] = None
    batch_index: Optional[int] = None
    word_count: Optional[int] = None
    token_count: Optional[int] = None
    resource_url: Optional[str] = None
    process_start_at: Optional[str] = None
    process_end_at: Optional[str] = None
    parse_start_at: Optional[str] = None
    parse_end_at: Optional[str] = None
    split_start_at: Optional[bool] = None
    split_end_at: Optional[int] = None

    document_segments: List[DocumentSegmentSchema] = Field(default_factory=list)

    @classmethod
    def from_orm(cls, obj: Document):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            dataset_uuid=str(obj.dataset_uuid),
            tenant_uuid=str(obj.tenant_uuid),
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            title=obj.title,
            status=obj.status,
            type=obj.type,
            document_index=obj.document_index,
            batch_index=obj.batch_index,
            word_count=obj.word_count,
            token_count=obj.token_count,
            resource_url=obj.resource_url,
            process_start_at=obj.process_start_at,
            process_end_at=obj.process_end_at,
            parse_start_at=obj.parse_start_at,
            parse_end_at=obj.parse_end_at,
            split_start_at=obj.split_start_at,
            split_end_at=obj.split_end_at,

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
