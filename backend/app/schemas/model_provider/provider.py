from typing import Optional

from openai import BaseModel
from pydantic import UUID4, constr
from datetime import datetime

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider import ConfigurateMethod, ModelCredentialEntity, CustomConfigurationStatus, Help, ProviderCredentialEntity
from app.models.model_provider.provider import ProviderType
from app.models.model_provider.provider_model import ModelType

from app.schemas.base import BaseSchema


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
    help: Optional[Help] = None
    supported_model_types: list[ModelType]
    configurate_methods: list[ConfigurateMethod]
    provider_credential_schema: Optional[ProviderCredentialEntity] = None
    model_credential_schema: Optional[ModelCredentialEntity] = None
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
    data: dict
