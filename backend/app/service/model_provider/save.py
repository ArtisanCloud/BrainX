import json

from sqlalchemy.orm import Session

from app.core.brainx.provider_manager import ProviderManager
from app.models import Provider
from app.models.model_provider.provider import ProviderType
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
        provider_manager = ProviderManager(sync_db=sync_db)

        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)

        # 获取指定的provider配置
        provider_configuration = configurations.get(provider)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider}")

        # 验证 credentials 是否有效
        provider_record, credentials = provider_configuration.validate_provider_credentials(credentials)

        # upsert credentials
        provider_service = ProviderService(sync_db=sync_db)
        if provider_record:
            dict_provider_record: dict = {}
            # print("update provider record")
            dict_provider_record["encrypted_config"] = json.dumps(credentials)
            dict_provider_record["is_valid"] = True
            # print(dict_provider_record)
            provider_record, exception = provider_service.provider_dao.sync_patch(
                provider_record.uuid, dict_provider_record
            )
        else:
            # print("create provider record")
            provider_record = Provider()
            provider_record.tenant_uuid = tenant_uuid
            provider_record.provider_name = provider
            provider_record.provider_type = ProviderType.CUSTOM.value
            provider_record.encrypted_config = json.dumps(credentials)
            provider_record.is_valid = True
            provider_record, exception = provider_service.provider_dao.sync_create(
                provider_record
            )
        if exception:
            raise exception

    except Exception as e:
        return None, e

    return provider_record, None
