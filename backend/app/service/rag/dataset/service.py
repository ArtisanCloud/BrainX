from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.dataset import DatasetDAO


class DatasetService:
    def __init__(self, db: AsyncSession):
        self.app_dao = DatasetDAO(db)
