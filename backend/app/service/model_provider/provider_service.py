from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import settings
from app.core.ai_model.provider_manager import ProviderManager
from app.core.ai_model.schema.provider import ProviderSchema
from app.core.rag import FrameworkDriverType

from app.dao.model_provider.provider import ProviderDAO
from app.models.model_provider.provider import Provider


class ProviderService:
    def __init__(self, async_db: AsyncSession):
        self.model_provider_dao = ProviderDAO(async_db)
        self.provider_manager = ProviderManager(
            FrameworkDriverType(settings.agent.framework_driver)
        )


def transform_provider_to_reply(provider: Provider) -> [ProviderSchema | None]:
    if provider is None:
        return None

    return ProviderSchema.from_orm(provider)
