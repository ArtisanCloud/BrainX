from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.document_segment import DocumentSegmentDAO


class DocumentSegmentService:
    def __init__(self, db: AsyncSession):
        self.app_dao = DocumentSegmentDAO(db)
