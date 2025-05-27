from sqlalchemy.ext.asyncio import AsyncSession
from app import logger
from app.models.model_provider.provider import Provider
from app.schemas.model_provider.provider import ProviderSchema
from app.service.model_provider.provider_service import (
    ProviderService,
    transform_provider_to_reply,
)
from typing import Tuple
from app.config.config import settings


async def save_model_provider(
        async_db: AsyncSession,
        tenant_uuid: str,
        provider_name: str,
        credentials: dict
) -> Tuple[ProviderSchema | None, Exception | None]:
    try:
        service_model_provider = ProviderService(async_db)

        _, _ = await service_model_provider.provider_manager.get_provider_configuration(tenant_uuid, provider_name)

        model_provider = None
        # model_provider, exception = (
        #     await service_model_provider.model_provider_dao.async_create(model_provider)
        # )
        # if exception:
        #     raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        return None, e

    return transform_provider_to_reply(model_provider), None
