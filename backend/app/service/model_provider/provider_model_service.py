import json
from typing import Tuple, List, Union, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import logger
from app.core.brainx.entity.provider_config import ProviderConfiguration
from app.core.brainx.entity.provider_model import ModelWithProviderEntity, ModelStatus, ProviderModelWithStatusEntity
from app.core.brainx.entity.runtime.provider import ModelCredentialSchema, ProviderCredentialSchema
from app.core.brainx.entity.runtime.provider_model import ModelType, ParameterRule
from app.core.brainx.provider_manager import ProviderManager
from app.dao.model_provider.provider_model import ProviderModelDAO, ProviderModelSettingDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.models import ProviderModel
from app.models.model_provider.provider_model import ProviderModelSetting
from app.models.tenant.tenant import TenantDefaultModel
from app.schemas.model_provider.provider import ModelWithProviderEntityResponse, CustomConfigurationStatus, SimpleProviderEntityResponse
from app.schemas.model_provider.provider_model import ProviderModelSchema, ProviderWithModelsResponse, DefaultModelResponse
from app.utils.cache.provider_credentials import ProviderCredentialsCache, ProviderCredentialsCacheType
from app.utils.encrypter import get_decrypt_decoding, decrypt_content_with_decoding


class ProviderModelService:
    async_db: AsyncSession
    sync_db: Session
    provider_model_dao: ProviderModelDAO

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.provider_model_dao = ProviderModelDAO(async_db=async_db, sync_db=sync_db)
        self.provider_model_setting_dao = ProviderModelSettingDAO(async_db=async_db, sync_db=sync_db)
        self.sync_db = sync_db
        self.async_db = async_db

    def get_models_by_provider(self, tenant_uuid: str, provider_id: str) -> List[ModelWithProviderEntityResponse]:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        configurations = provider_manager.get_configurations(tenant_uuid)

        all_models = configurations.get_models(provider=provider_id)
        models = []

        for provider_model in all_models:
            models.append(ModelWithProviderEntityResponse(
                tenant_uuid=tenant_uuid,
                provider_model=provider_model
            ))
        return models

    def save_model_credentials(
            self, tenant_uuid: str, model_type: ModelType,
            provider: str, model: str, credentials: dict
    ) -> Tuple[ProviderModelSchema | None, Exception | None]:
        try:
            provider_manager = ProviderManager(sync_db=self.sync_db)

            # 加载租户的模型配置表
            configurations = provider_manager.get_configurations(tenant_uuid)

            # 获取指定的provider配置
            provider_configuration = configurations.get(provider)
            if provider_configuration is None:
                raise Exception(f"Cannot find provider configuration for {provider}")

            # 验证 credentials 是否有效
            provider_model_record, credentials = provider_configuration.validate_provider_model_credentials(
                model_type=model_type, model=model, credentials=credentials
            )
            # print(provider_model_record, credentials)

            if provider_model_record:
                dict_provider_model_record: dict = {}
                dict_provider_model_record["encrypted_config"] = json.dumps(credentials)
                dict_provider_model_record["is_valid"] = True
                provider_model_record, exception = self.provider_model_dao.sync_update(
                    provider_model_record.uuid, dict_provider_model_record
                )
            else:
                provider_model_record = ProviderModel()
                provider_model_record.tenant_uuid = tenant_uuid
                provider_model_record.provider_name = provider
                provider_model_record.model_name = model
                provider_model_record.model_type = model_type.value
                provider_model_record.encrypted_config = json.dumps(credentials)
                provider_model_record.is_valid = True
                provider_model_record, exception = self.provider_model_dao.sync_create(
                    provider_model_record
                )

            if exception:
                raise exception

            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid,
                identity_id=provider_model_record.uuid,
                cache_type=ProviderCredentialsCacheType.MODEL,
            )
            provider_model_credentials_cache.delete()

            if exception:
                raise exception

        except Exception as e:
            return None, e

        return provider_model_record, None

    def _get_credential_schema(
            self, provider_configuration: ProviderConfiguration
    ) -> Union[ModelCredentialSchema, ProviderCredentialSchema]:
        """Get form schemas."""
        if provider_configuration.provider.model_credential_schema:
            return provider_configuration.provider.model_credential_schema
        elif provider_configuration.provider.provider_credential_schema:
            return provider_configuration.provider.provider_credential_schema
        else:
            raise ValueError("No credential schema found")

    def get_model_credentials(
            self, tenant_uuid: str, model_type: str, provider: str, model: str,
    ) -> Tuple[dict | None, Exception | None]:
        provider_manager = ProviderManager(sync_db=self.sync_db)

        # Get all provider configurations of the current workspace
        provider_configurations = provider_manager.get_configurations(tenant_uuid)

        # Get provider configuration
        provider_configuration = provider_configurations.get(provider)
        if not provider_configuration:
            return None, Exception(f"Cannot find provider configuration for {provider}")

        return provider_configuration.get_custom_model_credentials(
            model_type=ModelType(model_type), model=model, desensitized=True
        ), None

    def change_status(self, tenant_uuid: str, provider: str, model_type: str, model_id: str, status: bool):
        provider_manager = ProviderManager(sync_db=self.sync_db)

        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)

        # 获取指定的provider配置
        provider_configuration = configurations.get(provider)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider}")

        model_setting = provider_configuration.get_provider_model_setting(model_type=ModelType(model_type), model=model_id)

        if model_setting:
            dict_model_setting: dict = {}
            dict_model_setting["enabled"] = status
            model_setting, exception = self.provider_model_setting_dao.sync_patch(
                model_setting.uuid, dict_model_setting
            )
        else:
            model_setting = ProviderModelSetting()
            model_setting.tenant_uuid = tenant_uuid
            model_setting.provider_name = provider
            model_setting.model_type = model_type
            model_setting.model_name = model_id
            model_setting.enabled = status
            model_setting, exception = self.provider_model_setting_dao.sync_create(model_setting)

        if exception:
            raise exception

        return model_setting

    def delete_model(self, tenant_uuid: str, provider_id: str, model_type: str, model_id: str) -> Exception | None:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        # 加载租户的模型配置表
        configurations = provider_manager.get_configurations(tenant_uuid)
        # 获取指定的provider配置
        provider_configuration = configurations.get(provider_id)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider_id}")

        provider_configuration.delete_custom_model_credentials(model_type=ModelType(model_type), model=model_id)

        return None

    def get_models_by_model_type(self, tenant_uuid: str, model_type: str) -> list[ProviderWithModelsResponse]:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        provider_configurations = provider_manager.get_configurations(tenant_uuid)

        # Get provider available models
        models = provider_configurations.get_models(model_type=ModelType(model_type))

        # Group models by provider
        provider_models: dict[str, list[ModelWithProviderEntity]] = {}
        for model in models:
            if model.provider.provider not in provider_models:
                provider_models[model.provider.provider] = []

            if model.deprecated:
                continue

            if model.status != ModelStatus.ACTIVE:
                continue

            provider_models[model.provider.provider].append(model)

        # convert to ProviderWithModelsResponse list
        providers_with_models: list[ProviderWithModelsResponse] = []
        for provider, models in provider_models.items():
            if not models:
                continue

            first_model = models[0]

            providers_with_models.append(
                ProviderWithModelsResponse(
                    tenant_uuid=tenant_uuid,
                    provider=provider,
                    label=first_model.provider.label,
                    icon_small=first_model.provider.icon_small,
                    icon_large=first_model.provider.icon_large,
                    status=CustomConfigurationStatus.ACTIVE,
                    models=[
                        ProviderModelWithStatusEntity(
                            model=model.model,
                            label=model.label,
                            model_type=model.model_type,
                            features=model.features,
                            fetch_from=model.fetch_from,
                            model_properties=model.model_properties,
                            status=model.status,
                            load_balancing_enabled=model.load_balancing_enabled,
                        )
                        for model in models
                    ],
                )
            )

        return providers_with_models

    def get_default_model_of_model_type(self, tenant_uuid: str, model_type: str) -> Optional[DefaultModelResponse]:

        model_type_enum = ModelType(model_type)
        provider_manager = ProviderManager(sync_db=self.sync_db)

        try:
            result = provider_manager.get_default_model(tenant_uuid=tenant_uuid, model_type=model_type_enum)

            return (
                DefaultModelResponse(
                    model=result.model,
                    model_type=result.model_type,
                    provider=SimpleProviderEntityResponse(
                        tenant_uuid=tenant_uuid,
                        provider=result.provider.provider,
                        label=result.provider.label,
                        icon_small=result.provider.icon_small,
                        icon_large=result.provider.icon_large,
                        supported_model_types=result.provider.supported_model_types,
                    ),
                )
                if result
                else None
            )
        except Exception as e:
            logger.debug(f"get_default_model_of_model_type error: {e}")
            return None

    def update_default_model_of_model_type(self, tenant_uuid: str, model_type: str, model: str, provider: str):
        model_type_enum = ModelType(model_type)
        provider_manager = ProviderManager(sync_db=self.sync_db)
        provider_configurations = provider_manager.get_configurations(tenant_uuid)
        if provider not in provider_configurations:
            raise ValueError(f"Provider {provider} does not exist.")

        # get available models from provider_configurations
        available_models = provider_configurations.get_models(model_type=model_type_enum, only_active=True)

        # check if the model is exist in available models
        model_names = [model.model for model in available_models]
        if model not in model_names:
            raise ValueError(f"Model {model} does not exist.")

        # Get the list of available models from get_configurations and check if it is LLM
        tenant_default_model_dao = TenantDefaultModelDAO(sync_db=self.sync_db)
        default_model, exception = tenant_default_model_dao.sync_get_by({
            "tenant_uuid": tenant_uuid,
            "type": model_type_enum.value,
        })
        if exception:
            return None, exception

        # create or update TenantDefaultModel record
        if default_model:
            dict_default_model_setting: dict = {}
            # update default model
            dict_default_model_setting["provider_name"] = provider
            dict_default_model_setting["name"] = model
            default_model, exception = tenant_default_model_dao.sync_patch(default_model.uuid, dict_default_model_setting)
            if exception:
                return None, exception
        else:
            # create default model
            default_model = TenantDefaultModel(
                tenant_uuid=tenant_uuid,
                type=model_type,
                provider_name=provider,
                name=model,
            )
            default, exception = tenant_default_model_dao.sync_create(default_model)
            if exception:
                return None, exception

        return default_model, None

    def get_model_parameter_rules(self, tenant_uuid: str, model: str, provider: str) -> list[ParameterRule]:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        provider_configurations = provider_manager.get_configurations(tenant_uuid)
        provider_configuration = provider_configurations.get(provider)
        if not provider_configuration:
            raise ValueError(f"Provider {provider} does not exist.")

        # fetch credentials
        credentials = provider_configuration.get_current_credentials(model_type=ModelType.LLM, model=model)

        if not credentials:
            return []

        model_schema = provider_configuration.get_model_schema(
            model_type=ModelType.LLM, model=model, credentials=credentials
        )

        return model_schema.parameter_rules if model_schema else []
