from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import Enum
from typing import Optional
from app.core.ai_model.entity.provider import ProviderEntity

from app.models.model_provider.provider_model import ModelType
from app.schemas.model_provider.provider_model import ProviderModelSchema


class AIModel(ABC):
    """
    Base class for all models.
    """

    model_id = Enum
    provider_model_type: ModelType
    provider_schema: ProviderEntity
    provider_model_schemas: Optional[list[ProviderModelSchema]] = None
    started_at: float = 0

    # pydantic configs
    class Config:
        protected_namespaces = ()

    @abstractmethod
    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self) -> any:
        raise NotImplementedError
