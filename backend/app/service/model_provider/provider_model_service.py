from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.dao.model_provider.provider_model import ProviderModelDAO


class ProviderModelService:
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.provider_model_dao = ProviderModelDAO(async_db=async_db, sync_db=sync_db)

    def get_models_by_provider(self, tenant_uuid: str, provider_id: str) -> Tuple[list, Exception]:
        models, exception = self.provider_model_dao.sync_get_by({
            "tenant_uuid": tenant_uuid,
            "provider_id": provider_id
        })
        return models, exception
