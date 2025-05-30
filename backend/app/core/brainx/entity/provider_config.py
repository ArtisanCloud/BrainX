from typing import Optional, Iterator

from pydantic import BaseModel, ConfigDict, Field

from app.core.brainx.drivers.factory import ModelProviderFactory
from app.core.brainx.entity.provider import ProviderEntity, SystemConfiguration, CustomConfiguration
from app.core.brainx.entity.provider_model import ProviderModelEntity
from app.core.brainx.interface.ai_model import AIModel
from app.models.model_provider.provider import ProviderType
from app.models.model_provider.provider_model import ModelType


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
        model_provider_factory = ModelProviderFactory(self.tenant_uuid)

        # Get model instance of LLM
        return model_provider_factory.get_model_type_instance(
            model_type=model_type,
            provider_id=provider_id,
            model_id=model_id,
        )


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
