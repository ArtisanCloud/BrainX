from collections import defaultdict
from typing import Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session

from app.core.brainx.entity.base import ModelProviderID
from app.core.brainx.entity.provider_bundle import ProviderModelBundle
from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.entity.provider_config import ProviderConfigurations, ProviderConfiguration, ModelSettings
from app.core.brainx.entity.provider import ProviderEntity
from app.core.brainx.providers.registry import ModelProviderRegistry

from app.dao.model_provider.provider import ProviderDAO
from app.dao.model_provider.provider_model import ProviderModelDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.models.model_provider.provider import ProviderType
from app.models.model_provider.provider_model import ModelType, ProviderModel
from app.models.tenant.tenant import TenantDefaultModel


class ProviderManager:
    async_db: AsyncSession
    sync_db: Session
    model_provider_dao: ProviderDAO

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.async_db = async_db
        self.sync_db = sync_db
        self.model_provider_dao = ProviderDAO(async_db=async_db, sync_db=sync_db)
        self.model_provider_model_dao = ProviderModelDAO(async_db=async_db, sync_db=sync_db)

    def get_default_model(
            self, tenant_uuid: str, model_type: ModelType
    ) -> Tuple[Optional[TenantDefaultModel], Optional[Exception]]:
        try:
            # 获取默认模型
            service_tenant_default_model = TenantDefaultModelDAO(sync_db=self.sync_db)
            default_model, exception = (
                service_tenant_default_model.get_default_model_by_uuid(
                    tenant_uuid, model_type.value
                )
            )

            if exception is not None:
                raise exception

            if default_model is None:
                raise Exception("Cannot query the default_model")

        except Exception as e:
            # 记录异常或打印日志（可选）
            return None, e

        return default_model, None

    def get_provider_model_bundle(self, tenant_uuid: str, provider: str, model_type: ModelType):
        # 加载租户的模型配置表
        configurations = self.get_configurations(tenant_uuid)

        # 获取指定的provider配置
        provider_configuration = configurations.get(provider)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider}")

        # 通过配置对象，获取指定的模型实例
        model_instance = provider_configuration.get_model_type_instance(model_type)

        return ProviderModelBundle(
            configuration=provider_configuration,
            model_type_instance=model_instance,
        ), None

    def get_all_providers(self, tenant_uuid: str) -> Dict[str, ProviderEntity]:
        provider_records, exception = self.model_provider_dao.sync_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "is_valid": True,
        })
        dict_providers = defaultdict(list)
        for record in provider_records:
            dict_providers[record.provider_name].append(record)

        return dict_providers

    def get_all_provider_models(self, tenant_uuid: str) -> Dict[str, ProviderEntity]:
        provider_model_records, exception = self.model_provider_model_dao.sync_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "is_valid": True,
        })
        if exception is not None:
            raise Exception(exception)

        dict_provider_models = defaultdict(list)
        for record in provider_model_records:
            dict_provider_models[record.provider_name].append(record)

        return dict_provider_models

    def get_configurations(self, tenant_uuid: str) -> ProviderConfigurations:

        # 查询租户的provider配置表
        dict_providers = self.get_all_providers(tenant_uuid)

        # 查询租户的模型配置表
        dict_provider_models = self.get_all_provider_models(tenant_uuid)

        # 加载系统的模型配置表
        dict_provider_entities, exception = ModelProviderRegistry.load_provider_entities()
        if exception:
            raise Exception(exception)
        # print(dict_provider_entities["openai"])
        provider_configurations = ProviderConfigurations(tenant_uuid=tenant_uuid)

        for key, provider_entity in dict_provider_entities.items():
            provider_name = provider_entity.provider
            provider_records = dict_providers.get(provider_entity.provider, [])
            provider_model_records = dict_provider_models.get(provider_entity.provider, [])
            provider_id_entity = ModelProviderID(provider_name)

            using_provider_type = ProviderType.SYSTEM

            # Convert to model settings
            model_settings = self._to_model_settings(
                provider_models=provider_model_records,
                # provider_entity=provider_entity,
                # load_balancing_model_configs=provider_load_balancing_configs,
            )

            provider_configuration = ProviderConfiguration(
                tenant_uuid=tenant_uuid,
                provider=provider_entity,
                preferred_provider_type=using_provider_type,
                using_provider_type=using_provider_type,
                # system_configuration=system_configuration,
                # custom_configuration=custom_configuration,
                model_settings=model_settings,
            )
            provider_configurations[str(provider_id_entity)] = provider_configuration

        return provider_configurations

    def _to_model_settings(
            self,
            provider_models: Optional[list[ProviderModel]] = None,
            # self, provider_entity: ProviderEntity,
            # load_balancing_model_configs: Optional[list[LoadBalancingModelConfig]] = None,
    ):
        model_settings: list[ModelSettings] = []
        if not provider_models:
            return model_settings

        for provider_model in provider_models:
            model_settings.append(
                ModelSettings(
                    model=provider_model.model_name,
                    model_type=ModelType(provider_model.model_type),
                    enabled=provider_model.is_valid,
                    # load_balancing_configs=load_balancing_configs if len(load_balancing_configs) > 1 else [],
                )
            )

    def get_first_provider_first_model(self, tenant_uuid: str, model_type: ModelType) -> tuple[str | None, str | None]:
        return None, None

    @staticmethod
    def convert_default_model_to_model(
            self, default_model: ProviderModel
    ) -> Tuple[Optional[AIModel], Optional[Exception]]:
        return None, None

    def get_provider_configurations(self, tenant_uuid: str) -> ProviderConfigurations | None:
        return None
