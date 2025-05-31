import json
from json import JSONDecodeError
from typing import Optional, Iterator

from pydantic import BaseModel, ConfigDict, Field

from app.constant import HIDDEN_VALUE
from app.core.brainx.drivers.provider_model_factory import ProviderModelFactory

from app.core.brainx.drivers.provider_factory import ProviderFactory
from app.core.brainx.entity.base import FormType
from app.core.brainx.entity.provider import ProviderEntity, SystemConfiguration, CustomConfiguration, CredentialFormSchema
from app.core.brainx.entity.provider_model import ProviderModelEntity
from app.core.brainx.interface.ai_model import AIModel
from app.database.session_manager import get_sync_db_session
from app.models.model_provider.provider import ProviderType, Provider
from app.models.model_provider.provider_model import ModelType
from app.service.model_provider.provider_service import ProviderService
from app.service.tenant.service import TenantService


class ModelSettings(BaseModel):
    """
    Model class for model settings.
    """

    model: str
    model_type: ModelType
    enabled: bool = True
    # load_balancing_configs: list[ModelLoadBalancingConfiguration] = []

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())


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

    def extract_secret_variables(self, credential_form_schemas: list[CredentialFormSchema]) -> list[str]:
        secret_input_form_variables = []
        for credential_form_schema in credential_form_schemas:
            # print(credential_form_schema.type)
            if credential_form_schema.type == FormType.INPUT_SECRET:
                secret_input_form_variables.append(credential_form_schema.variable)

        return secret_input_form_variables

    def validate_provider_credentials(self, credentials: dict) -> tuple[Provider | None, dict]:
        provider_record = None
        with get_sync_db_session() as sync_db:
            provider_dao = ProviderService(sync_db=sync_db).provider_dao
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
                        credentials[key] = tenant_service.decrypt_content(self.tenant_uuid, original_credentials[key])
            # print("credentials:", credentials)

        # validate credentials
        provider_factory = ProviderFactory(tenant_uuid=self.tenant_uuid)
        credentials = provider_factory.provider_credentials_validate(
            provider_id=self.provider.provider, credentials=credentials
        )
        # print(credentials)

        tenant_service = TenantService(sync_db=sync_db)
        for key, value in credentials.items():
            if key in provider_credential_secret_variables:
                credentials[key] = tenant_service.encrypt_content(self.tenant_uuid, value)
        # print(provider_record, credentials)

        return provider_record, credentials


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
    ) -> list[ProviderModelEntity]:

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
