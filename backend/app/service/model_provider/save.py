from sqlalchemy.orm import Session

from app.schemas.model_provider.provider import ProviderSchema
from app.service.model_provider.provider_service import (
    ProviderService,
    transform_provider_to_reply,
)
from typing import Tuple
from app.config.config import settings


async def save_model_provider(
        sync_db: Session,
        tenant_uuid: str,
        provider: str,
        credentials: dict
) -> Tuple[ProviderSchema | None, Exception | None]:
    try:
        service_model_provider = ProviderService(sync_db=sync_db)

        # 加载租户的模型配置表
        configurations = service_model_provider.provider_manager.get_configurations(tenant_uuid)

        # 获取指定的provider配置
        provider_configuration = configurations.get(provider)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider}")

        model_provider = None
        # model_provider, exception = (
        #     await service_model_provider.model_provider_dao.async_create(model_provider)
        # )
        # if exception:
        #     raise exception

    except Exception as e:
        return None, e

    return transform_provider_to_reply(model_provider), None
