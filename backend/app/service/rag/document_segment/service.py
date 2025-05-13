from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.document_segment import DocumentSegmentDAO
from app.models.rag.document_segment import DocumentSegment
from app.schemas.rag.document_segment import DocumentSegmentSchema


class DocumentSegmentService:
    def __init__(self,async_db: AsyncSession):
        self.app_dao = DocumentSegmentDAO(async_db)


def transform_document_segments_to_reply(
    document_segments: [DocumentSegment],
) -> List[DocumentSegmentSchema]:
    if document_segments is None:
        return []
    data = [
        transform_document_segment_to_reply(resource) for resource in document_segments
    ]
    # print(data)
    return data


def transform_document_segment_to_reply(
    document_segment: DocumentSegment,
) -> [DocumentSegmentSchema | None]:
    if document_segment is None:
        return None

    return DocumentSegmentSchema.from_orm(document_segment)
