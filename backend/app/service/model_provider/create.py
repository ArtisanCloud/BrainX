from sqlalchemy.ext.asyncio import AsyncSession
from app import logger
from app.models.model_provider.provider import Provider
from app.schemas.model_provider.provider import ProvderSchema
from app.service.model_provider.provider_service import (
    ProviderService,
    transform_provider_to_reply,
)
from typing import Tuple
from app.config.config import settings


async def create_model_provider(
   async_db: AsyncSession,
    model_provider: Provider,
) -> Tuple[ProvderSchema | None, Exception | None]:
    try:
        service_model_provider = ProviderService(async_db)

        service_model_provider.provider_manager.get_model()

        model_provider, exception = (
            await service_model_provider.model_provider_dao.async_create(model_provider)
        )
        if exception:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        return None, e

    return transform_provider_to_reply(model_provider), None
