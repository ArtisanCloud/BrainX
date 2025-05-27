from pydantic import BaseModel, ConfigDict

from app.core.ai_model.drivers.interface.ai_model import AIModel
from app.core.ai_model.entity.provider_config import ProviderConfiguration


class ProviderModelBundle(BaseModel):
    """
    Provider model bundle.
    """

    configuration: ProviderConfiguration
    model_type_instance: AIModel

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())
