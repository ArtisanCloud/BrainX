from enum import Enum
from typing import Optional

from openai import BaseModel
from pydantic import UUID4, constr
from datetime import datetime

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider_model import ProviderModelWithStatusEntity, ModelWithProviderEntity
from app.core.brainx.entity.runtime.provider import ProviderHelpEntity, ConfigurateMethod, ProviderCredentialSchema, ModelCredentialSchema, SimpleProviderEntity, ProviderEntity
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.models.model_provider.provider import ProviderType

from app.schemas.base import BaseSchema


class SimpleProviderEntityResponse(SimpleProviderEntity):
    tenant_uuid: str


class ModelWithProviderEntityResponse(ProviderModelWithStatusEntity):
    provider: SimpleProviderEntityResponse

    def __init__(self, tenant_uuid: str, provider_model: ModelWithProviderEntity) -> None:
        dump_model = provider_model.model_dump()
        dump_model["provider"]["tenant_uuid"] = tenant_uuid
        super().__init__(**dump_model)


class CustomConfigurationStatus(Enum):
    ACTIVE = "active"
    NO_CONFIGURE = "no-configure"


class ProviderSchema(BaseSchema):
    tenant_uuid: UUID4
    provider_name: constr(min_length=1)
    provider_type: constr(min_length=1)
    encrypted_config: Optional[str]
    is_valid: bool = False
    last_used: Optional[datetime]
    quota_type: Optional[int]
    quota_limit: Optional[int]
    quota_used: int = 0


class CustomConfigurationResponse(BaseModel):
    status: CustomConfigurationStatus


class ProviderResponse(BaseModel):
    tenant_uuid: str
    provider: str
    label: I18nObject
    description: Optional[I18nObject] = None
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    background: Optional[str] = None
    help: Optional[ProviderHelpEntity] = None
    supported_model_types: list[ModelType]
    configurate_methods: list[ConfigurateMethod]
    provider_credential_schema: Optional[ProviderCredentialSchema] = None
    model_credential_schema: Optional[ModelCredentialSchema] = None
    preferred_provider_type: ProviderType
    custom_configuration: CustomConfigurationResponse
    # system_configuration: SystemConfigurationResponse


class ResponseGetModelProviderList(BaseSchema):
    data: list[ProviderResponse]


class RequestCreateModelProvider(BaseSchema):
    config_from: str
    provider: str
    credentials: dict


class ResponseCreateModelProvider(BaseSchema):
    result: bool


class RequestDeleteModelProvider(BaseSchema):
    provider: str


class ResponseDeleteModelProvider(BaseSchema):
    result: bool


class RequestGetProviderCredentials(BaseSchema):
    provider: str


class ResponseGetProviderCredentials(BaseSchema):
    data: dict | None
