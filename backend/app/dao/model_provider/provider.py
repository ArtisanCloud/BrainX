from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.model_provider.provider import Provider


class ProviderDAO(BaseDAO[Provider]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Provider, async_db, sync_db)
