from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.app.app import AppDAO
from app.models import App


class AppService:
    def __init__(self, db: AsyncSession):
        self.app_dao = AppDAO(db)


