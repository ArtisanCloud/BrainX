from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.entity.provider_config import ProviderConfiguration


class ProviderModelBundle(BaseModel):
    """
    Provider model bundle.
    """

    configuration: ProviderConfiguration
    model_type_instance: AIModel

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())

    def get_credentials(self, model_id: str) -> Optional[dict]:
        # print("bundle credential:", self.configuration.custom_configuration, model_id)
        # print("bundle configuration:", self.configuration, model_id)
        if self.configuration.custom_configuration is not None:
            # print("provider get_credential:", self.configuration.custom_configuration.provider)
            if (
                    self.configuration.custom_configuration
                    and self.configuration.custom_configuration.provider
                    and self.configuration.custom_configuration.provider.credentials
            ):
                return self.configuration.custom_configuration.provider.credentials

            for model in self.configuration.custom_configuration.models:
                if model.model == model_id:
                    # print("model custom_configuration:", model.custom_configuration)
                    # print("model.credentials:", model.credentials)
                    if model.credentials is not None:
                        return model.credentials

        return None
