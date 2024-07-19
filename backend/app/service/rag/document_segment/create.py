from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.document_segment import DocumentSegmentSchema
from app.service.rag.document_segment.service import DocumentSegmentService

from app.models.rag.document_segment import DocumentSegment


def transform_document_segment_to_reply(document_segment: DocumentSegment) -> [DocumentSegmentSchema | None]:
    if document_segment is None:
        return None

    return DocumentSegmentSchema.from_orm(document_segment)


async def create_document_segment(
        db: AsyncSession,
        document_segment: DocumentSegment,
) -> Tuple[DocumentSegmentSchema | None, Exception | None]:
    service_document_segment = DocumentSegmentService(db)
    document_segment, exception = await service_document_segment.app_dao.create(document_segment)

    if exception:
        return None, exception

    return transform_document_segment_to_reply(document_segment), None
