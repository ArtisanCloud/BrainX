from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model_provider.provider_model import ProviderModel, ProviderModelSetting
from app.dao.base import BaseDAO


class ProviderModelDAO(BaseDAO[ProviderModel]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(ProviderModel, async_db, sync_db)


class ProviderModelSettingDAO(BaseDAO[ProviderModelSetting]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(ProviderModelSetting, async_db, sync_db)
