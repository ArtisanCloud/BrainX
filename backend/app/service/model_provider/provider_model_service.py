from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.model_provider.provider_model import ProviderModelDAO


class ProviderModelService:
    def __init__(self, async_db: AsyncSession):
        self.model_provider_dao = ProviderModelDAO(async_db)
