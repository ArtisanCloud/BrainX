import json
from collections import defaultdict
from json import JSONDecodeError
from typing import Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session

from app import logger, settings
from app.core.brainx.drivers.provider_model_factory import ProviderModelFactory
from app.core.brainx.entity.base import ModelProviderID
from app.core.brainx.entity.provider import CustomConfiguration, CustomProviderConfiguration, CustomModelConfiguration, ModelLoadBalancingConfiguration, SystemConfiguration, ProviderQuotaType
from app.core.brainx.entity.provider_bundle import ProviderModelBundle
from app.core.brainx.entity.provider_model import DefaultModelEntity, DefaultModelProviderEntity
from app.core.brainx.entity.runtime.provider import CredentialFormSchema, FormType, ProviderEntity, ConfigurateMethod
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.entity.provider_config import ProviderConfigurations, ProviderConfiguration, ModelSettings
from app.core.brainx.providers.registry import ModelProviderRegistry

from app.dao.model_provider.provider import ProviderDAO
from app.dao.model_provider.provider_model import ProviderModelDAO, ProviderModelSettingDAO
from app.dao.tenant.tenant import PreferredModelProviderDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.database.session_manager import get_sync_db_session
from app.models.model_provider.provider import ProviderType, Provider, LoadBalancingModelConfig
from app.models.model_provider.provider_model import ProviderModel, ProviderModelSetting
from app.models.tenant.tenant import TenantDefaultModel, TenantPreferredModelProvider
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
    ) -> Optional[DefaultModelEntity]:

        # 获取默认模型
        dao_tenant_default_model = TenantDefaultModelDAO(sync_db=self.sync_db)
        default_model, exception = (
            dao_tenant_default_model.get_default_model_by_uuid(
                tenant_uuid, model_type.value
            )
        )

        if exception is not None:
            raise exception

        # Get provider configurations
        provider_configurations = self.get_configurations(tenant_uuid)
        if not default_model:

            # get available models from provider_configurations
            available_models = provider_configurations.get_models(model_type=model_type, only_active=True)

            if available_models:
                available_model = next(
                    (model for model in available_models if model.model == "gpt-4"), available_models[0]
                )

                default_model = TenantDefaultModel()
                default_model.tenant_id = tenant_uuid
                default_model.type = model_type
                default_model.provider_name = available_model.provider.provider
                default_model.name = available_model.model
                dao_tenant_default_model.sync_create(default_model)

        if not default_model:
            return None

        provider_schema = provider_configurations[default_model.provider_name].provider

        return DefaultModelEntity(
            model=default_model.name,
            model_type=model_type,
            provider=DefaultModelProviderEntity(
                provider=provider_schema.provider,
                label=provider_schema.label,
                icon_small=provider_schema.icon_small,
                icon_large=provider_schema.icon_large,
                supported_model_types=provider_schema.supported_model_types,
            ),
        )

    def get_provider_model_bundle(
            self, tenant_uuid: str,
            model_type: ModelType, provider_id: str, model_id: str):
        # 加载租户的模型配置表
        configurations = self.get_configurations(tenant_uuid)
        # print("get_provider_model_bundle", configurations.configurations)
        # 获取指定的provider配置
        provider_configuration = configurations.get(provider_id)
        if provider_configuration is None:
            raise Exception(f"Cannot find provider configuration for {provider_id}")
        # print("provider_configuration:", provider_configuration)
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

    def get_all_preferred_model_providers(self, tenant_uuid: str) -> dict[str, TenantPreferredModelProvider]:
        with get_sync_db_session() as sync_db:
            preferred_model_provider_dao = PreferredModelProviderDAO(sync_db=sync_db)

            records, exception = preferred_model_provider_dao.sync_get_objects_by_conditions({
                "tenant_uuid": tenant_uuid,
            })
            if exception:
                raise exception

            dict_preferred_provider_type_records = {
                preferred_provider_type.provider_name: preferred_provider_type
                for preferred_provider_type in records
            }

            return dict_preferred_provider_type_records

    def get_all_provider_model_settings(self, tenant_uuid: str) -> dict[str, list[ProviderModelSetting]]:
        with get_sync_db_session() as sync_db:
            provider_model_setting_dao = ProviderModelSettingDAO(sync_db=sync_db)
            records, exception = provider_model_setting_dao.sync_get_objects_by_conditions({
                "tenant_uuid": tenant_uuid,
            })
            if exception:
                raise exception

            dict_provider_model_settings = defaultdict(list)
            for provider_model_setting in records:
                (
                    dict_provider_model_settings[provider_model_setting.provider_name].append(
                        provider_model_setting
                    )
                )

            return dict_provider_model_settings

    def get_all_provider_load_balancing_configs(self, tenant_uuid: str) -> dict:
        return {}

    @staticmethod
    def _get_all_preferred_model_providers(tenant_uuid: str) -> dict[str, TenantPreferredModelProvider]:
        with get_sync_db_session() as sync_db:
            preferred_model_provider_dao = PreferredModelProviderDAO(sync_db=sync_db)
            preferred_provider_types, exception = preferred_model_provider_dao.sync_get_objects_by_conditions({
                "tenant_uuid": tenant_uuid,
            })
            if exception:
                raise exception

            provider_name_to_preferred_provider_type_records_dict = {
                preferred_provider_type.provider_name: preferred_provider_type
                for preferred_provider_type in preferred_provider_types
            }

            return provider_name_to_preferred_provider_type_records_dict

    def get_configurations(self, tenant_uuid: str) -> ProviderConfigurations:

        # 查询租户的provider配置表
        dict_providers = self.get_all_providers(tenant_uuid)
        # print(dict_providers)
        # 查询租户的模型配置表
        dict_provider_models = self.get_all_provider_models(tenant_uuid)

        # 加载系统的模型配置表
        dict_provider_entities, exception = ModelProviderRegistry.load_provider_entities()
        if exception:
            logger.error(
                f"Failed to load provider entities for tenant {tenant_uuid}: {exception}", exc_info=settings.log.exc_info
            )
            raise Exception(exception)

        # Get All preferred provider types of the workspace
        dict_preferred_model_provider_records = self.get_all_preferred_model_providers(tenant_uuid=tenant_uuid)
        # Ensure that both the original provider name and its ModelProviderID string representation
        # are present in the dictionary to handle cases where either form might be used
        for provider_id in list(dict_preferred_model_provider_records.keys()):
            # provider_id = ModelProviderID(provider_name)
            if str(provider_id) not in dict_preferred_model_provider_records:
                # Add the ModelProviderID string representation if it's not already present
                dict_preferred_model_provider_records[str(provider_id)] = (
                    dict_preferred_model_provider_records[provider_id]
                )

        # Get All provider model settings
        dict_provider_model_settings = self.get_all_provider_model_settings(tenant_uuid=tenant_uuid)

        # Get All preferred provider types of the workspace
        provider_name_to_preferred_model_provider_records_dict = self._get_all_preferred_model_providers(tenant_uuid)
        # Ensure that both the original provider name and its ModelProviderID string representation
        # are present in the dictionary to handle cases where either form might be used
        for provider_name in list(provider_name_to_preferred_model_provider_records_dict.keys()):
            provider_id = ModelProviderID(provider_name)
            if str(provider_id) not in provider_name_to_preferred_model_provider_records_dict:
                # Add the ModelProviderID string representation if it's not already present
                provider_name_to_preferred_model_provider_records_dict[str(provider_id)] = (
                    provider_name_to_preferred_model_provider_records_dict[provider_name]
                )

        # Get All load balancing configs
        dict_load_balancing_model_configs = self.get_all_provider_load_balancing_configs(
            tenant_uuid
        )

        provider_configurations = ProviderConfigurations(tenant_uuid=tenant_uuid)

        for key, provider_entity in dict_provider_entities.items():
            # print(provider_entity.provider, len(provider_entity.models))

            provider_name = provider_entity.provider
            provider_records = dict_providers.get(provider_entity.provider, [])
            provider_model_records = dict_provider_models.get(provider_entity.provider, [])
            # provider_id_entity = ModelProviderID(provider_name)
            provider_id_entity = provider_name

            custom_configuration = self._to_custom_configuration(
                tenant_uuid, provider_entity, provider_records, provider_model_records
            )

            # Convert to system configuration
            system_configuration = self._to_system_configuration(tenant_uuid, provider_entity, provider_records)

            # Get preferred provider type
            preferred_provider_type_record = provider_name_to_preferred_model_provider_records_dict.get(provider_name)

            if preferred_provider_type_record:
                preferred_provider_type = ProviderType(preferred_provider_type_record.preferred_provider_type)
            elif custom_configuration.provider or custom_configuration.models:
                preferred_provider_type = ProviderType.CUSTOM
            elif system_configuration.enabled:
                preferred_provider_type = ProviderType.SYSTEM
            else:
                preferred_provider_type = ProviderType.CUSTOM

            using_provider_type = preferred_provider_type

            provider_model_settings = dict_provider_model_settings.get(provider_name)

            # Get provider load balancing configs
            provider_load_balancing_configs = dict_load_balancing_model_configs.get(
                provider_name
            )

            # Convert to model settings
            model_settings = self._to_model_settings(
                provider_entity=provider_entity,
                provider_model_settings=provider_model_settings,
                load_balancing_model_configs=provider_load_balancing_configs,
            )

            provider_configuration = ProviderConfiguration(
                tenant_uuid=tenant_uuid,
                provider=provider_entity,
                preferred_provider_type=preferred_provider_type,
                using_provider_type=using_provider_type,
                system_configuration=system_configuration,
                custom_configuration=custom_configuration,
                model_settings=model_settings,
            )
            provider_configurations[str(provider_id_entity)] = provider_configuration

        return provider_configurations

    def _to_model_settings(
            self,
            provider_entity: ProviderEntity,
            provider_model_settings: Optional[list[ProviderModelSetting]] = None,
            load_balancing_model_configs: Optional[list[LoadBalancingModelConfig]] = None,
    ):
        # Get provider model credential secret variables
        if ConfigurateMethod.PREDEFINED_MODEL in provider_entity.configurate_methods:
            model_credential_secret_variables = self._extract_secret_variables(
                provider_entity.provider_credential_schema.credential_form_schemas
                if provider_entity.provider_credential_schema
                else []
            )
        else:
            model_credential_secret_variables = self._extract_secret_variables(
                provider_entity.model_credential_schema.credential_form_schemas
                if provider_entity.model_credential_schema
                else []
            )

        model_settings: list[ModelSettings] = []
        if not provider_model_settings:
            return model_settings

        for provider_model_setting in provider_model_settings:
            load_balancing_configs = []
            if provider_model_setting.load_balancing_enabled and load_balancing_model_configs:
                for load_balancing_model_config in load_balancing_model_configs:
                    if (
                            load_balancing_model_config.model_name == provider_model_setting.model_name
                            and load_balancing_model_config.model_type == provider_model_setting.model_type
                    ):
                        if not load_balancing_model_config.enabled:
                            continue

                        if not load_balancing_model_config.encrypted_config:
                            if load_balancing_model_config.name == "__inherit__":
                                load_balancing_configs.append(
                                    ModelLoadBalancingConfiguration(
                                        id=load_balancing_model_config.id,
                                        name=load_balancing_model_config.name,
                                        credentials={},
                                    )
                                )
                            continue

                        provider_model_credentials_cache = ProviderCredentialsCache(
                            tenant_uuid=load_balancing_model_config.tenant_uuid,
                            identity_id=load_balancing_model_config.id,
                            cache_type=ProviderCredentialsCacheType.LOAD_BALANCING_MODEL,
                        )

                        # Get cached provider model credentials
                        cached_provider_model_credentials = provider_model_credentials_cache.get()
                        print("cached cached_provider_model_credentials", cached_provider_model_credentials)
                        if not cached_provider_model_credentials:
                            try:
                                provider_model_credentials = json.loads(load_balancing_model_config.encrypted_config)
                            except JSONDecodeError:
                                continue

                            # Get decoding rsa key and cipher for decrypting credentials
                            if self.decoding_rsa_key is None or self.decoding_cipher_rsa is None:
                                self.decoding_rsa_key, self.decoding_cipher_rsa = get_decrypt_decoding(
                                    load_balancing_model_config.tenant_id
                                )

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

                        load_balancing_configs.append(
                            ModelLoadBalancingConfiguration(
                                id=load_balancing_model_config.id,
                                name=load_balancing_model_config.name,
                                credentials=provider_model_credentials,
                            )
                        )

            model_settings.append(
                ModelSettings(
                    model=provider_model_setting.model_name,
                    model_type=ModelType(provider_model_setting.model_type),
                    enabled=provider_model_setting.enabled,
                    load_balancing_configs=load_balancing_configs if len(load_balancing_configs) > 1 else [],
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

    def _to_system_configuration(
            self, tenant_uuid: str, provider_entity: ProviderEntity, provider_records: list[Provider]
    ) -> SystemConfiguration:

        quota_type_to_provider_records_dict = {}
        for provider_record in provider_records:
            # print("provider_record", provider_record)
            if provider_record.provider_type != ProviderType.SYSTEM.value:
                continue

            quota_type_to_provider_records_dict[ProviderQuotaType.value_of(provider_record.quota_type)] = (
                provider_record
            )

        return SystemConfiguration(
            enabled=True,
            # current_quota_type=current_quota_type,
            # quota_configurations=quota_configurations,
            # credentials=current_using_credentials,
        )

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
            # print("provider_record:", provider_record)
            if provider_record.provider_type == ProviderType.SYSTEM.value:
                continue

            if not provider_record.encrypted_config:
                continue

            custom_provider_record = provider_record
            # print("custom_provider_record:", custom_provider_record)

        # Get custom provider credentials
        custom_provider_configuration = None
        # print("tenant_uuid:", tenant_uuid)
        # print("custom_provider_record:", custom_provider_record)
        if custom_provider_record:
            provider_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid,
                identity_id=custom_provider_record.uuid,
                cache_type=ProviderCredentialsCacheType.PROVIDER,
            )

            # Get cached provider credentials
            cached_provider_credentials = provider_credentials_cache.get()
            # print("cached_provider_credentials:", cached_provider_credentials)
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
                except JSONDecodeError as e:
                    logger.error(e, exc_info=settings.log.exc_info)
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

            # print("provider credentials:", provider_credentials)
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
