import json
from json import JSONDecodeError
from typing import Optional, Iterator, Sequence
from collections import defaultdict

from pydantic import BaseModel, ConfigDict, Field

from app import logger
from app.constant import HIDDEN_VALUE
from app.core.brainx.drivers.provider_model_factory import ProviderModelFactory

from app.core.brainx.drivers.provider_factory import ProviderFactory
from app.core.brainx.entity.provider import SystemConfiguration, CustomConfiguration, ModelSettings
from app.core.brainx.entity.provider_model import ModelWithProviderEntity, ModelStatus, FetchFrom, SimpleModelProviderEntity
from app.core.brainx.entity.runtime.provider import ProviderEntity, FormType, CredentialFormSchema
from app.core.brainx.entity.runtime.provider_model import ModelType, AIModelEntity
from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.providers.registry import ModelProviderRegistry
from app.dao.model_provider.provider import ProviderDAO
from app.dao.model_provider.provider_model import ProviderModelDAO, ProviderModelSettingDAO
from app.database.session_manager import get_sync_db_session
from app.models.model_provider.provider import ProviderType, Provider
from app.models.model_provider.provider_model import ProviderModel
from app.service.tenant.service import TenantService
from app.utils.cache.provider_credentials import ProviderCredentialsCache, ProviderCredentialsCacheType
from app.utils.encrypter import decrypt_content, encrypt_content, desensitized_content


class ProviderConfiguration(BaseModel):
    """
    Model class for provider configuration.
    """

    tenant_uuid: str
    provider: ProviderEntity
    preferred_provider_type: ProviderType
    using_provider_type: ProviderType
    system_configuration: SystemConfiguration = None
    custom_configuration: CustomConfiguration = None
    model_settings: list[ModelSettings]

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())

    def get_model_type_instance(self, model_type: ModelType, provider_id: str = None, model_id: str = None) -> AIModel:
        """
        Get current model type instance.

        :param model_type: model type
        :param model_id: model id
        :return:
        """
        model_provider_factory = ProviderModelFactory(self.tenant_uuid)

        # Get model instance of LLM
        return model_provider_factory.get_model_type_instance(
            model_type=model_type,
            provider_id=provider_id,
            model_id=model_id,
        )

    def is_custom_configuration_available(self) -> bool:
        return self.custom_configuration.provider is not None or len(self.custom_configuration.models) > 0

    def get_provider_model_setting(self, model_type: ModelType, model: str) -> Optional[ModelSettings]:
        with get_sync_db_session() as sync_db:
            provider_model_setting_dao = ProviderModelSettingDAO(sync_db=sync_db)
            provider_model_record, exception = provider_model_setting_dao.sync_get_by({
                "tenant_uuid": self.tenant_uuid,
                "provider_name": self.provider.provider,
                "model_name": model,
                "model_type": model_type.value,
            })
            # print("fetch provider record", provider_record)
            if exception:
                raise exception

            return provider_model_record

    def extract_secret_variables(self, credential_form_schemas: list[CredentialFormSchema]) -> list[str]:
        secret_input_form_variables = []
        for credential_form_schema in credential_form_schemas:
            # print(credential_form_schema.type)
            if credential_form_schema.type == FormType.INPUT_SECRET:
                secret_input_form_variables.append(credential_form_schema.variable)

        return secret_input_form_variables

    def validate_provider_credentials(
            self, credentials: dict,
    ) -> tuple[Provider | None, dict]:
        provider_record = None
        with get_sync_db_session() as sync_db:
            provider_dao = ProviderDAO(sync_db=sync_db)
            provider_record, exception = provider_dao.sync_get_by({
                "tenant_uuid": self.tenant_uuid,
                "provider_type": ProviderType.CUSTOM.value,
                "provider_name": self.provider.provider,
            })
            # print("fetch provider record", provider_record)
            if exception:
                raise exception

        # Get provider credential secret variables
        provider_credential_secret_variables = self.extract_secret_variables(
            self.provider.provider_credential_schema.credential_form_schemas
            if self.provider.provider_credential_schema
            else []
        )
        # print(provider_credential_secret_variables)

        if provider_record:
            try:
                # fix origin data
                if provider_record.encrypted_config:
                    if not provider_record.encrypted_config.startswith("{"):
                        original_credentials = {"openai_api_key": provider_record.encrypted_config}
                    else:
                        original_credentials = json.loads(provider_record.encrypted_config)
                else:
                    original_credentials = {}
            except JSONDecodeError:
                original_credentials = {}

            # encrypt credentials
            tenant_service = TenantService(sync_db=sync_db)
            for key, value in credentials.items():
                if key in provider_credential_secret_variables:
                    # if send [__HIDDEN__] in secret input, it will be same as original value
                    if value == HIDDEN_VALUE and key in original_credentials:
                        credentials[key] = decrypt_content(self.tenant_uuid, original_credentials[key])
            # print("credentials:", credentials)

        # validate credentials
        provider_factory = ProviderFactory(tenant_uuid=self.tenant_uuid)
        credentials = provider_factory.provider_credentials_validate(
            provider_id=self.provider.provider, credentials=credentials
        )
        # print(credentials)

        for key, value in credentials.items():
            if key in provider_credential_secret_variables:
                credentials[key] = encrypt_content(sync_db, self.tenant_uuid, value)
        # print(provider_record, credentials)

        return provider_record, credentials

    def validate_provider_model_credentials(
            self, model_type: ModelType, model: str, credentials: dict
    ) -> tuple[ProviderModel | None, dict]:
        provider_model_record = None
        with get_sync_db_session() as sync_db:
            provider_model_dao = ProviderModelDAO(sync_db=sync_db)
            provider_model_record, exception = provider_model_dao.sync_get_by({
                "tenant_uuid": self.tenant_uuid,
                "provider_name": self.provider.provider,
                "model_name": model,
                "model_type": model_type.value,
            })
            # print("fetch provider record", provider_record)
            if exception:
                raise exception
        provider_credential_secret_variables = self.extract_secret_variables(
            self.provider.model_credential_schema.credential_form_schemas
            if self.provider.model_credential_schema
            else []
        )

        if provider_model_record:
            try:
                original_credentials = (
                    json.loads(provider_model_record.encrypted_config) if provider_model_record.encrypted_config else {}
                )
            except JSONDecodeError:
                original_credentials = {}

            # decrypt credentials
            for key, value in credentials.items():
                if key in provider_credential_secret_variables:
                    # if send [__HIDDEN__] in secret input, it will be same as original value
                    if value == HIDDEN_VALUE and key in original_credentials:
                        credentials[key] = decrypt_content(self.tenant_uuid, original_credentials[key])

        provider_factory = ProviderFactory(tenant_uuid=self.tenant_uuid)
        credentials = provider_factory.model_credentials_validate(
            provider_id=self.provider.provider, model_type=model_type,
            model_id=model, credentials=credentials
        )

        for key, value in credentials.items():
            if key in provider_credential_secret_variables:
                credentials[key] = encrypt_content(self.tenant_uuid, value)

        return provider_model_record, credentials

    def desensitized_credentials(self, credentials: dict, credential_form_schemas: list[CredentialFormSchema]) -> dict:
        # Get provider credential secret variables
        credential_secret_variables = self.extract_secret_variables(credential_form_schemas)

        # Obfuscate provider credentials
        copy_credentials = credentials.copy()
        for key, value in copy_credentials.items():
            if key in credential_secret_variables:
                copy_credentials[key] = desensitized_content(value)

        return copy_credentials

    def get_custom_credentials(self, desensitized: bool = False) -> dict | None:
        if self.custom_configuration.provider is None:
            return None

        credentials = self.custom_configuration.provider.credentials
        if not desensitized:
            return credentials

        return self.desensitized_credentials(
            credentials=credentials,
            credential_form_schemas=self.provider.provider_credential_schema.credential_form_schemas
            if self.provider.provider_credential_schema
            else [],
        )

    def delete_custom_credentials(self) -> None:
        # get provider
        with get_sync_db_session() as sync_db:
            provider_dao = ProviderDAO(sync_db=sync_db)

            record_uuid, exception = provider_dao.sync_delete_by({
                "tenant_uuid": self.tenant_uuid,
                "provider_type": ProviderType.CUSTOM.value,
                "provider_name": self.provider.provider,
            })
            if exception:
                raise exception

            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=self.tenant_uuid,
                identity_id=record_uuid,
                cache_type=ProviderCredentialsCacheType.PROVIDER,
            )

            provider_model_credentials_cache.delete()

    def delete_custom_model_credentials(self, model_type: ModelType, model: str) -> None:
        # get provider
        with get_sync_db_session() as sync_db:
            provider_model_dao = ProviderModelDAO(sync_db=sync_db)
            record_uuid, exception = provider_model_dao.sync_delete_by({
                "tenant_uuid": self.tenant_uuid,
                "model_type": model_type.value,
                "provider_name": self.provider.provider,
                "model_name": model,

            })
            if exception:
                raise exception
            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=self.tenant_uuid,
                identity_id=record_uuid,
                cache_type=ProviderCredentialsCacheType.MODEL,
            )
            provider_model_credentials_cache.delete()

    def get_provider_models(
            self, model_type: Optional[ModelType] = None, only_active: bool = False, model: Optional[str] = None
    ) -> list[ModelWithProviderEntity]:

        dict_provider_entities, exception = ModelProviderRegistry.load_provider_entities()
        if exception:
            raise Exception(exception)
        provider_schema = dict_provider_entities.get(self.provider.provider)

        model_types: list[ModelType] = []
        if model_type:
            model_types.append(model_type)
        else:
            model_types = list(provider_schema.supported_model_types)

        # Group model settings by model type and model
        model_setting_map: defaultdict[ModelType, dict[str, ModelSettings]] = defaultdict(dict)
        for model_setting in self.model_settings:
            model_setting_map[model_setting.model_type][model_setting.model] = model_setting

        # Get provider models
        provider_models = []

        if self.using_provider_type == ProviderType.SYSTEM:
            # provider_models = self._get_system_provider_models(
            #     model_types=model_types, provider_schema=provider_schema, model_setting_map=model_setting_map
            # )
            pass
        else:
            provider_models = self._get_custom_provider_models(
                model_types=model_types,
                provider_schema=provider_schema,
                model_setting_map=model_setting_map,
                model=model,
            )

        if only_active:
            provider_models = [m for m in provider_models if m.status == ModelStatus.ACTIVE]

        # resort provider_models
        if hasattr(self.provider, "position") and self.provider.position:
            model_type_positions = self.provider.position

        def get_sort_key(model: ModelWithProviderEntity):
            return (model.model_type.value, model.model.lower())

        # Sort using the composite sort key
        return sorted(provider_models, key=get_sort_key)

    def get_model_schema(self, model_type: ModelType, model: str, credentials: dict) -> AIModelEntity | None:
        model_instance = self.get_model_type_instance(model_type=model_type, provider_id=self.provider.provider, model_id=model)
        return model_instance.get_customizable_model_schema_from_credentials(model=model, credentials=credentials)

    def get_custom_model_credentials(
            self, model_type: ModelType, model: str, desensitized: bool = False
    ) -> Optional[dict]:

        if not self.custom_configuration.models:
            return None

        for model_configuration in self.custom_configuration.models:
            if model_configuration.model_type == model_type and model_configuration.model == model:
                credentials = model_configuration.credentials
                if not desensitized:
                    return credentials

                # Obfuscate credentials
                return self.desensitized_credentials(
                    credentials=credentials,
                    credential_form_schemas=self.provider.model_credential_schema.credential_form_schemas
                    if self.provider.model_credential_schema
                    else [],
                )

        return None

    def _get_custom_provider_models(
            self,
            model_types: Sequence[ModelType],
            provider_schema: ProviderEntity,
            model_setting_map: dict[ModelType, dict[str, ModelSettings]],
            model: Optional[str] = None,
    ) -> list[ModelWithProviderEntity]:

        provider_models = []

        credentials = None
        if self.custom_configuration.provider:
            credentials = self.custom_configuration.provider.credentials

        for model_type in model_types:
            if model_type not in self.provider.supported_model_types:
                continue

            for m in provider_schema.models:
                if m.model_type != model_type:
                    continue

                status = ModelStatus.ACTIVE if credentials else ModelStatus.NO_CONFIGURE

                load_balancing_enabled = False
                if m.model_type in model_setting_map and m.model in model_setting_map[m.model_type]:
                    model_setting = model_setting_map[m.model_type][m.model]
                    if model_setting.enabled is False:
                        status = ModelStatus.DISABLED

                    if len(model_setting.load_balancing_configs) > 1:
                        load_balancing_enabled = True

                provider_models.append(
                    ModelWithProviderEntity(
                        model=m.model,
                        label=m.label,
                        model_type=m.model_type,
                        features=m.features,
                        fetch_from=m.fetch_from,
                        model_properties=m.model_properties,
                        deprecated=m.deprecated,
                        provider=SimpleModelProviderEntity(self.provider),
                        status=status,
                        load_balancing_enabled=load_balancing_enabled,
                    )
                )

        # custom models
        for model_configuration in self.custom_configuration.models:
            if model_configuration.model_type not in model_types:
                continue
            if model and model != model_configuration.model:
                continue

            try:
                custom_model_schema = self.get_model_schema(
                    model_type=model_configuration.model_type,
                    model=model_configuration.model,
                    credentials=model_configuration.credentials,
                )

            except Exception as ex:
                logger.warning(f"get custom model schema failed, {ex}")
                continue

            if not custom_model_schema:
                continue

            status = ModelStatus.ACTIVE
            load_balancing_enabled = False
            if (
                    custom_model_schema.model_type in model_setting_map
                    and custom_model_schema.model in model_setting_map[custom_model_schema.model_type]
            ):
                model_setting = model_setting_map[custom_model_schema.model_type][custom_model_schema.model]
                if model_setting.enabled is False:
                    status = ModelStatus.DISABLED

                if len(model_setting.load_balancing_configs) > 1:
                    load_balancing_enabled = True

            provider_models.append(
                ModelWithProviderEntity(
                    model=custom_model_schema.model,
                    label=custom_model_schema.label,
                    model_type=custom_model_schema.model_type,
                    features=custom_model_schema.features,
                    fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
                    model_properties=custom_model_schema.model_properties,
                    deprecated=custom_model_schema.deprecated,
                    provider=SimpleModelProviderEntity(self.provider),
                    status=status,
                    load_balancing_enabled=load_balancing_enabled,
                )
            )

        return provider_models

    def get_current_credentials(self, model_type: ModelType, model: str) -> Optional[dict]:
        if self.model_settings:
            # check if model is disabled by admin
            for model_setting in self.model_settings:
                if model_setting.model_type == model_type and model_setting.model == model:
                    if not model_setting.enabled:
                        raise ValueError(f"Model {model} is disabled.")

        if self.using_provider_type == ProviderType.SYSTEM:
            restrict_models = []
            for quota_configuration in self.system_configuration.quota_configurations:
                if self.system_configuration.current_quota_type != quota_configuration.quota_type:
                    continue

                restrict_models = quota_configuration.restrict_models

            copy_credentials = (
                self.system_configuration.credentials.copy() if self.system_configuration.credentials else {}
            )
            if restrict_models:
                for restrict_model in restrict_models:
                    if (
                            restrict_model.model_type == model_type
                            and restrict_model.model == model
                            and restrict_model.base_model_name
                    ):
                        copy_credentials["base_model_name"] = restrict_model.base_model_name

            return copy_credentials
        else:
            credentials = None
            if self.custom_configuration.models:
                for model_configuration in self.custom_configuration.models:
                    if model_configuration.model_type == model_type and model_configuration.model == model:
                        credentials = model_configuration.credentials
                        break

            if not credentials and self.custom_configuration.provider:
                credentials = self.custom_configuration.provider.credentials

            return credentials


class ProviderConfigurations(BaseModel):
    """
    Model class for provider configuration dict.
    """

    tenant_uuid: str
    configurations: dict[str, ProviderConfiguration] = Field(default_factory=dict)

    def __init__(self, tenant_uuid: str):
        super().__init__(tenant_uuid=tenant_uuid)

    def get_models(
            self, provider: Optional[str] = None, model_type: Optional[ModelType] = None, only_active: bool = False
    ) -> list[ModelWithProviderEntity]:

        all_models = []
        for provider_configuration in self.values():
            if provider and provider_configuration.provider.provider != provider:
                continue
            all_models.extend(provider_configuration.get_provider_models(model_type, only_active))

        return all_models

    def to_list(self) -> list[ProviderConfiguration]:
        """
        Convert to list.

        :return:
        """
        return list(self.values())

    def __getitem__(self, key):
        # if "/" not in key:
        #     key = str(ModelProviderID(key))

        return self.configurations[key]

    def __setitem__(self, key, value):
        self.configurations[key] = value

    def __iter__(self):
        return iter(self.configurations)

    def values(self) -> Iterator[ProviderConfiguration]:
        return iter(self.configurations.values())

    def get(self, key, default=None) -> ProviderConfiguration | None:
        return self.configurations.get(key, default)  # type: ignore
