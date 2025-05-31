from abc import abstractmethod
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict

from app.models.model_provider.provider_model import ModelType


class AIModel(BaseModel):
    """
    Base class for all models.
    """

    tenant_uuid: str
    model_id: str
    model_type: ModelType
    provider_name: str
    # provider_entity: ProviderEntity
    started_at: float = 0

    model_config = ConfigDict(protected_namespaces=())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def validate_credentials(self, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self, params: dict = None) -> any:
        raise NotImplementedError
