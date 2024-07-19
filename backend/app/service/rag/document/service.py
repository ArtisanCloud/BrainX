from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.document import DocumentDAO


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.app_dao = DocumentDAO(db)
