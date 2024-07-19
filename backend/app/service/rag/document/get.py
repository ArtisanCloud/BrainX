from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document


async def get_document_by_id(
        db: AsyncSession,
        document_id: int
) -> Document:
    return await db.get(Document, document_id)
