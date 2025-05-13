from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rag.document_segment import DocumentSegment


async def get_document_segment_by_id(
        async_db: AsyncSession,
        document_segment_id: int
) -> DocumentSegment:
    document_segment, err = await async_db.get(DocumentSegment, document_segment_id)
    return document_segment
