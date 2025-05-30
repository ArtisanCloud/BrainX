from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.config.config import settings
from app.core.brainx.provider_manager import ProviderManager
from app.core.brainx.entity.provider import ProviderEntity

from app.dao.model_provider.provider import ProviderDAO
from app.models.model_provider.provider import Provider


class ProviderService:
    model_provider_dao: ProviderDAO

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.model_provider_dao = ProviderDAO(async_db=async_db, sync_db=sync_db)
        self.provider_manager = ProviderManager(async_db=async_db, sync_db=sync_db)

    async def get_provider(self, tenant_uuid: str, provider_name: str) -> Tuple[Provider | None, Exception | None]:
        providers, exception = await self.model_provider_dao.async_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "provider_name": provider_name,
        })
        if exception:
            return None, exception

        # logger.info(providers)

        return providers, None


def transform_provider_to_reply(provider: Provider) -> [ProviderEntity | None]:
    if provider is None:
        return None

    return ProviderEntity.from_orm(provider)
