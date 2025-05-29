from abc import ABC, abstractmethod
from collections.abc import Mapping

from app.core.brainx.entity.provider import ProviderEntity
from app.models.model_provider.provider_model import ModelType


class AIModel(ABC):
    """
    Base class for all models.
    """

    tenant_uuid: str
    model_type: ModelType
    model_id: str
    provider_name: str
    provider_entity: ProviderEntity
    started_at: float = 0

    # pydantic configs
    class Config:
        protected_namespaces = ()

    @abstractmethod
    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self, params: dict = None) -> any:
        raise NotImplementedError
