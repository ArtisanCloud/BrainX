import json
from typing import Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.brainx.entity.runtime.provider import ProviderEntity
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.provider_manager import ProviderManager

from app.dao.model_provider.provider import ProviderDAO
from app.models.model_provider.provider import Provider, ProviderType

from app.schemas.model_provider.provider import ProviderResponse, CustomConfigurationResponse, ProviderSchema, CustomConfigurationStatus
from app.utils.cache.provider_credentials import ProviderCredentialsCache, ProviderCredentialsCacheType


class ProviderService:
    async_db: AsyncSession
    sync_db: Session
    model_provider_dao: ProviderDAO

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.provider_dao = ProviderDAO(async_db=async_db, sync_db=sync_db)
        self.sync_db = sync_db
        self.async_db = async_db

    def get_provider_list(self, tenant_uuid: str, model_type: str) -> Tuple[Optional[list[ProviderResponse]], Optional[Exception]]:
        provider_manager = ProviderManager(sync_db=self.sync_db)

        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)
        provider_responses = []
        for provider_configuration in configurations.values():
            if model_type:
                model_type_entity = ModelType(model_type)
                if model_type_entity not in provider_configuration.provider.supported_model_types:
                    continue

            provider_response = ProviderResponse(
                tenant_uuid=tenant_uuid,
                provider=provider_configuration.provider.provider,
                label=provider_configuration.provider.label,
                description=provider_configuration.provider.description,
                icon_small=provider_configuration.provider.icon_small,
                icon_large=provider_configuration.provider.icon_large,
                background=provider_configuration.provider.background,
                help=provider_configuration.provider.help,
                supported_model_types=provider_configuration.provider.supported_model_types,
                configurate_methods=provider_configuration.provider.configurate_methods,
                provider_credential_schema=provider_configuration.provider.provider_credential_schema,
                model_credential_schema=provider_configuration.provider.model_credential_schema,
                preferred_provider_type=provider_configuration.preferred_provider_type,
                custom_configuration=CustomConfigurationResponse(
                    status=CustomConfigurationStatus.ACTIVE
                    if provider_configuration.is_custom_configuration_available()
                    else CustomConfigurationStatus.NO_CONFIGURE
                ),
                # system_configuration=SystemConfigurationResponse(
                #     enabled=provider_configuration.system_configuration.enabled,
                #     current_quota_type=provider_configuration.system_configuration.current_quota_type,
                #     quota_configurations=provider_configuration.system_configuration.quota_configurations,
                # ),
            )

            provider_responses.append(provider_response)

        return provider_responses, None

    async def get_provider(self, tenant_uuid: str, provider_name: str) -> Tuple[Provider | None, Exception | None]:
        providers, exception = await self.model_provider_dao.async_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "provider_name": provider_name,
        })
        if exception:
            return None, exception

        # logger.info(providers)

        return providers, None

    def save_model_provider_credentials(
            self,
            tenant_uuid: str,
            provider: str,
            credentials: dict
    ) -> Tuple[ProviderSchema | None, Exception | None]:
        try:
            provider_manager = ProviderManager(sync_db=self.sync_db)

            # 加载租户的模型配置表
            configurations = provider_manager.get_configurations(tenant_uuid)

            # 获取指定的provider配置
            provider_configuration = configurations.get(provider)
            if provider_configuration is None:
                raise Exception(f"Cannot find provider configuration for {provider}")

            # 验证 credentials 是否有效
            provider_record, credentials = provider_configuration.validate_provider_credentials(credentials)

            # upsert credentials
            if provider_record:
                dict_provider_record: dict = {}
                # print("update provider record", )
                dict_provider_record["encrypted_config"] = json.dumps(credentials)
                dict_provider_record["is_valid"] = True
                # print(dict_provider_record["encrypted_config"])
                provider_record, exception = self.provider_dao.sync_patch(
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
                provider_record, exception = self.provider_dao.sync_create(
                    provider_record
                )

            if exception:
                raise exception

            # 清楚缓存
            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid, identity_id=provider_record.uuid, cache_type=ProviderCredentialsCacheType.PROVIDER
            )
            provider_model_credentials_cache.delete()

            if exception:
                raise exception

        except Exception as e:
            return None, e

        return provider_record, None

    def get_provider_credentials(self, tenant_uuid: str, provider_id: str) -> Tuple[dict | None, Exception | None]:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)
        # 获取指定的provider配置
        provider_configuration = configurations.get(provider_id)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider_id}")

        return provider_configuration.get_custom_credentials(desensitized=True), None

    def delete_provider(self, tenant_uuid: str, provider_id: str) -> Exception | None:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)
        # 获取指定的provider配置
        provider_configuration = configurations.get(provider_id)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider_id}")

        provider_configuration.delete_custom_credentials()

        return None


def transform_provider_to_reply(provider: Provider) -> [ProviderEntity | None]:
    if provider is None:
        return None

    return ProviderEntity.from_orm(provider)
