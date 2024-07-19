from typing import Optional

from pydantic import constr

from app.models.rag.document_segment import DocumentSegment
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema


class DocumentSegmentSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    document_uuid: Optional[str] = None
    dataset_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    status: Optional[int] = None
    content: Optional[str] = None
    document_index: Optional[int] = None
    word_count: Optional[int] = None
    token_count: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: DocumentSegment):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            tenant_uuid=obj.tenant_uuid,
            document_uuid=str(obj.document_uuid),
            dataset_uuid=str(obj.dataset_uuid),
            created_user_by=obj.created_user_by,
            updated_user_by=obj.updated_user_by,
            status=obj.status,
            content=obj.content,
            document_index=obj.document_index,
            word_count=obj.word_count,
            token_count=obj.token_count,
        )


class RequestGetDocumentSegmentList(BaseSchema):
    pagination: Optional[Pagination] = None


class ResponseGetDocumentSegmentList(BaseSchema):
    data: list[DocumentSegmentSchema]
    pagination: ResponsePagination


class RequestCreateDocumentSegment(DocumentSegmentSchema):
    name: constr(min_length=1)
    description: constr(min_length=1)


class ResponseCreateDocumentSegment(BaseSchema):
    document_segment: DocumentSegmentSchema


class RequestPatchDocumentSegment(DocumentSegmentSchema):
    pass


class ResponsePatchDocumentSegment(BaseSchema):
    document_segment: DocumentSegmentSchema


class ResponseDeleteDocumentSegment(BaseSchema):
    result: bool


def make_document_segment(document_segment: DocumentSegmentSchema) -> DocumentSegment:
    return DocumentSegment(
        tenant_uuid=document_segment.tenant_uuid,
        document_uuid=document_segment.document_uuid,
        dataset_uuid=document_segment.dataset_uuid,
        created_user_by=document_segment.created_user_by,
        updated_user_by=document_segment.updated_user_by,
        status=document_segment.status,
        content=document_segment.content,
        document_index=document_segment.document_index,
        word_count=document_segment.word_count,
        token_count=document_segment.token_count,
    )
