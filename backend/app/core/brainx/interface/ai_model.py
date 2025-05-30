from abc import ABC, abstractmethod
from collections.abc import Mapping

from pydantic import BaseModel

from app.core.brainx.entity.provider import ProviderEntity
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # pydantic configs
    class Config:
        protected_namespaces = ()

    @abstractmethod
    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self, params: dict = None) -> any:
        raise NotImplementedError
