from typing import Optional, List

from pydantic import constr, Field

from app.models.rag.document import Document
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema
from app.schemas.rag.document_segment import DocumentSegmentSchema
from app.service.rag.document_segment.list import transform_document_segments_to_reply


class DocumentSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    import_type: Optional[int] = None
    driver_type: Optional[int] = None
    embedding_model: Optional[str] = None
    embedding_model_provider: Optional[str] = None
    document_segments: List[DocumentSegmentSchema] = Field(default_factory=list)

    @classmethod
    def from_orm(cls, obj: Document):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            tenant_uuid=obj.tenant_uuid,
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            name=obj.name,
            description=obj.description,
            is_published=obj.is_published,
            import_type=obj.import_type,
            driver_type=obj.driver_type,
            embedding_model=obj.embedding_model,
            document_segments=transform_document_segments_to_reply(obj.document_segments)
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
