from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.rag.document_segment.service import DocumentSegmentService


async def soft_delete_document_segment(
        db: AsyncSession,
        user_id: int,
        document_segment_uuid: str
) -> Tuple[bool | None, Exception | None]:
    service_document_segment = DocumentSegmentService(db)
    result, exception = await service_document_segment.soft_delete_document_segment(user_id, document_segment_uuid)

    if exception:
        return False, exception

    return result, None
