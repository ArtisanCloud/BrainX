from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.openapi.models.platform import Platform


class PlatformDAO(BaseDAO[Platform]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Platform, async_db, sync_db)
