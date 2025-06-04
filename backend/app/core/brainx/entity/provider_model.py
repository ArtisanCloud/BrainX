from enum import Enum
from typing import Optional, Any, Sequence

from pydantic import BaseModel, ConfigDict

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.runtime.provider import ProviderEntity
from app.core.brainx.entity.runtime.provider_model import ModelType, ModelFeature, FetchFrom, ModelPropertyKey, ProviderModel


class ModelStatus(Enum):
    """
    Enum class for model status.
    """

    ACTIVE = "active"
    NO_CONFIGURE = "no-configure"
    QUOTA_EXCEEDED = "quota-exceeded"
    NO_PERMISSION = "no-permission"
    DISABLED = "disabled"


class SimpleModelProviderEntity(BaseModel):
    """
    Simple provider.
    """

    provider: str
    label: I18nObject
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    supported_model_types: list[ModelType]

    def __init__(self, provider_entity: ProviderEntity) -> None:
        """
        Init simple provider.

        :param provider_entity: provider entity
        """
        super().__init__(
            provider=provider_entity.provider,
            label=provider_entity.label,
            icon_small=provider_entity.icon_small,
            icon_large=provider_entity.icon_large,
            supported_model_types=provider_entity.supported_model_types,
        )


class ProviderModelWithStatusEntity(ProviderModel):
    status: ModelStatus
    load_balancing_enabled: bool = False


class ModelWithProviderEntity(ProviderModelWithStatusEntity):
    provider: SimpleModelProviderEntity


class DefaultModelProviderEntity(BaseModel):
    """
    Default model provider entity.
    """

    provider: str
    label: I18nObject
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    supported_model_types: Sequence[ModelType] = []


class DefaultModelEntity(BaseModel):
    """
    Default model entity.
    """

    model: str
    model_type: ModelType
    provider: DefaultModelProviderEntity

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())
