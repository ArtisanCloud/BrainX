from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentSegment
from app.models.rag.document_segment import DocumentSegment


async def get_document_segment_by_id(
        db: AsyncSession,
        document_segment_id: int
) -> DocumentSegment:
    return await db.get(DocumentSegment, document_segment_id)
