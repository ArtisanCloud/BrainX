from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.dao.model_provider.provider_model import ProviderModelDAO


class ProviderModelService:
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.model_provider_dao = ProviderModelDAO(async_db=async_db, sync_db=sync_db)
