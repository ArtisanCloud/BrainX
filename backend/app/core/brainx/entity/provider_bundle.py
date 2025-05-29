from pydantic import BaseModel, ConfigDict

from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.entity.provider_config import ProviderConfiguration


class ProviderModelBundle(BaseModel):
    """
    Provider model bundle.
    """

    configuration: ProviderConfiguration
    model_instance: AIModel

    # pydantic configs
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())
