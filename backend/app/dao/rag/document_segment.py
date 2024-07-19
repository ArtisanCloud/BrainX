from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.rag.document_segment import DocumentSegment


class DocumentSegmentDAO(BaseDAO[DocumentSegment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DocumentSegment)
