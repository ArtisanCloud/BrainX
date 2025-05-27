from typing import Optional, Iterator

from llama_cpp.server.settings import ModelSettings
from pydantic import BaseModel, ConfigDict, Field

from app.core.ai_model.entity.provider import ProviderEntity, SystemConfiguration, CustomConfiguration
from app.core.ai_model.entity.provider_model import ProviderModelEntity
from app.models.model_provider.provider import ProviderType
from app.models.model_provider.provider_model import ModelType


class ProviderConfiguration(BaseModel):
    """
    Model class for provider configuration.
    """

    tenant_id: str
    provider: ProviderEntity
    preferred_provider_type: ProviderType
    using_provider_type: ProviderType
    system_configuration: SystemConfiguration
    custom_configuration: CustomConfiguration
    model_settings: list[ModelSettings]

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())


class ProviderConfigurations(BaseModel):
    """
    Model class for provider configuration dict.
    """

    tenant_id: str
    configurations: dict[str, ProviderConfiguration] = Field(default_factory=dict)

    def __init__(self, tenant_id: str):
        super().__init__(tenant_id=tenant_id)

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
        if "/" not in key:
            key = str(ModelProviderID(key))

        return self.configurations[key]

    def __setitem__(self, key, value):
        self.configurations[key] = value

    def __iter__(self):
        return iter(self.configurations)

    def values(self) -> Iterator[ProviderConfiguration]:
        return iter(self.configurations.values())

    def get(self, key, default=None) -> ProviderConfiguration | None:

        return self.configurations.get(key, default)  # type: ignore
