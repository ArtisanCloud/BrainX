from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.rag.document import Document


class DocumentDAO(BaseDAO[Document]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Document)
