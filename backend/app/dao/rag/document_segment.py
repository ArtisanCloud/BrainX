from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.models.rag.document_segment import DocumentSegment


class DocumentSegmentDAO(BaseDAO[DocumentSegment]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(DocumentSegment, async_db, sync_db)
