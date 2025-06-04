import json
from collections import defaultdict
from json import JSONDecodeError
from typing import Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session

from app.core.brainx.entity.provider import CustomConfiguration, CustomProviderConfiguration, CustomModelConfiguration
from app.core.brainx.entity.provider_bundle import ProviderModelBundle
from app.core.brainx.entity.runtime.provider import CredentialFormSchema, FormType, ProviderEntity
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.entity.provider_config import ProviderConfigurations, ProviderConfiguration, ModelSettings
from app.core.brainx.providers.registry import ModelProviderRegistry

from app.dao.model_provider.provider import ProviderDAO
from app.dao.model_provider.provider_model import ProviderModelDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.models.model_provider.provider import ProviderType, Provider
from app.models.model_provider.provider_model import ProviderModel
from app.models.tenant.tenant import TenantDefaultModel
from app.utils.cache.provider_credentials import ProviderCredentialsCache, ProviderCredentialsCacheType
from app.utils.encrypter import get_decrypt_decoding, decrypt_content_with_decoding


class ProviderManager:
    async_db: AsyncSession
    sync_db: Session
    provider_id: str = None
    model_id: str = None
    model_provider_dao: ProviderDAO
    decoding_rsa_key: str = None
    decoding_cipher_rsa: str = None

    def __init__(self,
                 async_db: AsyncSession = None, sync_db: Session = None,
                 provider_id=None, model_id=None,
                 ):
        self.async_db = async_db
        self.sync_db = sync_db
        self.provider_id = provider_id
        self.model_id = model_id
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

    def get_provider_model_bundle(
            self, tenant_uuid: str,
            model_type: ModelType, provider_id: str, model_id: str):
        # 加载租户的模型配置表
        configurations = self.get_configurations(tenant_uuid)
        # print(provider, configurations.configurations)
        # 获取指定的provider配置
        provider_configuration = configurations.get(provider_id)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider_id}")

        # 通过配置对象，获取指定的模型实例
        model_type_instance = provider_configuration.get_model_type_instance(
            model_type,
            provider_id=provider_id, model_id=model_id
        )

        return ProviderModelBundle(
            configuration=provider_configuration,
            model_type_instance=model_type_instance,
        ), None

    def get_all_providers(self, tenant_uuid: str) -> dict[str, list[Provider]]:
        provider_records, exception = self.model_provider_dao.sync_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "is_valid": True,
        })
        if exception is not None:
            raise Exception(exception)

        dict_providers = defaultdict(list)
        for record in provider_records:
            # print(111, record.provider_name, record.provider_type)
            dict_providers[record.provider_name].append(record)

        return dict_providers

    def get_all_provider_models(self, tenant_uuid: str) -> Dict[str, list[ProviderModel]]:
        provider_model_records, exception = self.model_provider_model_dao.sync_get_objects_by_conditions({
            "tenant_uuid": tenant_uuid,
            "is_valid": True,
        })
        if exception is not None:
            raise Exception(exception)

        dict_provider_models = defaultdict(list)
        for record in provider_model_records:
            # print(222, record.provider_name, record.model_name, record.model_type)
            dict_provider_models[record.provider_name].append(record)

        return dict_provider_models

    def get_configurations(self, tenant_uuid: str) -> ProviderConfigurations:

        # 查询租户的provider配置表
        dict_providers = self.get_all_providers(tenant_uuid)
        # print(dict_providers)
        # 查询租户的模型配置表
        dict_provider_models = self.get_all_provider_models(tenant_uuid)

        # 加载系统的模型配置表
        dict_provider_entities, exception = ModelProviderRegistry.load_provider_entities()
        if exception:
            raise Exception(exception)
        # print(dict_provider_entities["openai"])
        provider_configurations = ProviderConfigurations(tenant_uuid=tenant_uuid)

        for key, provider_entity in dict_provider_entities.items():
            # print(provider_entity.provider, len(provider_entity.models))

            provider_name = provider_entity.provider
            provider_records = dict_providers.get(provider_entity.provider, [])
            provider_model_records = dict_provider_models.get(provider_entity.provider, [])
            # provider_id_entity = ModelProviderID(provider_name)
            provider_id_entity = provider_name

            # using_provider_type = ProviderType.SYSTEM
            using_provider_type = ProviderType.CUSTOM

            custom_configuration = self._to_custom_configuration(
                tenant_uuid, provider_entity, provider_records, provider_model_records
            )

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
                custom_configuration=custom_configuration,
                model_settings=model_settings,
            )
            provider_configurations[str(provider_id_entity)] = provider_configuration
            # print(10333333, provider_configuration.provider.provider)

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

        return model_settings

    @staticmethod
    def _extract_secret_variables(credential_form_schemas: list[CredentialFormSchema]) -> list[str]:
        """
        Extract secret input form variables.

        :param credential_form_schemas:
        :return:
        """
        secret_input_form_variables = []
        for credential_form_schema in credential_form_schemas:
            if credential_form_schema.type == FormType.INPUT_SECRET:
                secret_input_form_variables.append(credential_form_schema.variable)

        return secret_input_form_variables

    def _to_custom_configuration(
            self,
            tenant_uuid: str,
            provider_entity: ProviderEntity,
            provider_records: list[Provider],
            provider_model_records: list[ProviderModel],
    ) -> CustomConfiguration:
        # Get provider credential secret variables
        provider_credential_secret_variables = self._extract_secret_variables(
            provider_entity.provider_credential_schema.credential_form_schemas
            if provider_entity.provider_credential_schema
            else []
        )

        # Get custom provider record
        custom_provider_record = None
        for provider_record in provider_records:
            if provider_record.provider_type == ProviderType.SYSTEM.value:
                continue

            if not provider_record.encrypted_config:
                continue

            custom_provider_record = provider_record

        # Get custom provider credentials
        custom_provider_configuration = None
        if custom_provider_record:
            provider_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid,
                identity_id=custom_provider_record.uuid,
                cache_type=ProviderCredentialsCacheType.PROVIDER,
            )

            # Get cached provider credentials
            cached_provider_credentials = provider_credentials_cache.get()

            if not cached_provider_credentials:
                try:
                    # fix origin data
                    if (
                            custom_provider_record.encrypted_config
                            and not custom_provider_record.encrypted_config.startswith("{")
                    ):
                        provider_credentials = {"openai_api_key": custom_provider_record.encrypted_config}
                    else:
                        provider_credentials = json.loads(custom_provider_record.encrypted_config)
                except JSONDecodeError:
                    provider_credentials = {}

                # Get decoding rsa key and cipher for decrypting credentials
                if self.decoding_rsa_key is None or self.decoding_cipher_rsa is None:
                    self.decoding_rsa_key, self.decoding_cipher_rsa = get_decrypt_decoding(tenant_uuid)

                for variable in provider_credential_secret_variables:
                    if variable in provider_credentials:
                        try:
                            provider_credentials[variable] = decrypt_content_with_decoding(
                                provider_credentials.get(variable) or "",  # type: ignore
                                self.decoding_rsa_key,
                                self.decoding_cipher_rsa,
                            )
                        except ValueError:
                            pass

                # cache provider credentials
                provider_credentials_cache.set(credentials=provider_credentials)
            else:
                provider_credentials = cached_provider_credentials

            custom_provider_configuration = CustomProviderConfiguration(credentials=provider_credentials)

        # Get provider model credential secret variables
        model_credential_secret_variables = self._extract_secret_variables(
            provider_entity.model_credential_schema.credential_form_schemas
            if provider_entity.model_credential_schema
            else []
        )

        # Get custom provider model credentials
        custom_model_configurations = []
        for provider_model_record in provider_model_records:
            if not provider_model_record.encrypted_config:
                continue

            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid, identity_id=provider_model_record.uuid, cache_type=ProviderCredentialsCacheType.MODEL
            )

            # Get cached provider model credentials
            cached_provider_model_credentials = provider_model_credentials_cache.get()

            if not cached_provider_model_credentials:
                try:
                    provider_model_credentials = json.loads(provider_model_record.encrypted_config)
                except JSONDecodeError:
                    continue

                # Get decoding rsa key and cipher for decrypting credentials
                if self.decoding_rsa_key is None or self.decoding_cipher_rsa is None:
                    self.decoding_rsa_key, self.decoding_cipher_rsa = get_decrypt_decoding(tenant_uuid)

                for variable in model_credential_secret_variables:
                    if variable in provider_model_credentials:
                        try:
                            provider_model_credentials[variable] = decrypt_content_with_decoding(
                                provider_model_credentials.get(variable),
                                self.decoding_rsa_key,
                                self.decoding_cipher_rsa,
                            )
                        except ValueError:
                            pass

                # cache provider model credentials
                provider_model_credentials_cache.set(credentials=provider_model_credentials)
            else:
                provider_model_credentials = cached_provider_model_credentials

            custom_model_configurations.append(
                CustomModelConfiguration(
                    model=provider_model_record.model_name,
                    model_type=ModelType(provider_model_record.model_type),
                    credentials=provider_model_credentials,
                )
            )
        return CustomConfiguration(provider=custom_provider_configuration, models=custom_model_configurations)

    def get_first_provider_first_model(self, tenant_uuid: str, model_type: ModelType) -> tuple[str | None, str | None]:
        return None, None

    @staticmethod
    def convert_default_model_to_model(
            self, default_model: ProviderModel
    ) -> Tuple[Optional[AIModel], Optional[Exception]]:
        return None, None

    def get_provider_configurations(self, tenant_uuid: str) -> ProviderConfigurations | None:
        return None
