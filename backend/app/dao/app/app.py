
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.app.app import App


class AppDAO(BaseDAO[App]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, App)
