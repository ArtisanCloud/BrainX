from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.rag.dataset import Dataset


class DatasetDAO(BaseDAO[Dataset]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Dataset)
