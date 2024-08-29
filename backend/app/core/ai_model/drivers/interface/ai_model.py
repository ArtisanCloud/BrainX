from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import Enum
from typing import Optional

from app.models.model_provider.provider_model import ModelType
from app.schemas.model_provider.model_provider import ProviderModelSchema


class AIModel(ABC):


    """
    Base class for all models.
    """
    model_id = Enum
    provider_model_type: ModelType
    provider_model_schemas: Optional[list[ProviderModelSchema]] = None
    started_at: float = 0

    # pydantic configs
    class Config:
        protected_namespaces = ()

    @abstractmethod
    def verify_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
