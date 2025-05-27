from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import settings
from app.core.ai_model.provider_manager import ProviderManager
from app.core.ai_model.entity.provider import ProviderEntity
from app.core.rag import FrameworkDriverType

from app.dao.model_provider.provider import ProviderDAO
from app.models.model_provider.provider import Provider


class ProviderService:
    def __init__(self, async_db: AsyncSession):
        self.model_provider_dao = ProviderDAO(async_db)
        self.provider_manager = ProviderManager(
            model_provider_dao=self.model_provider_dao,
            framework_type=FrameworkDriverType(settings.agent.framework_driver)
        )


def transform_provider_to_reply(provider: Provider) -> [ProviderEntity | None]:
    if provider is None:
        return None

    return ProviderEntity.from_orm(provider)
