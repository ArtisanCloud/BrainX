from typing import Optional
from pydantic import UUID4, constr, ConfigDict, BaseModel
from datetime import datetime

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider_model import ProviderModelWithStatusEntity
from app.core.brainx.entity.runtime.provider_model import ModelType, ParameterRule
from app.schemas.base import BaseSchema
from app.schemas.model_provider.load_balance import ModelLoadBalanceConfig
from app.schemas.model_provider.provider import ModelWithProviderEntityResponse, CustomConfigurationStatus, SimpleProviderEntityResponse


class ProviderModelSchema(BaseSchema):
    tenant_uuid: UUID4
    name: constr(min_length=1)
    mdl_name: constr(min_length=1)
    mdl_type: constr(min_length=1)
    encrypted_config: Optional[str]
    is_valid: bool = False
    last_used: Optional[datetime]

    quota_type: Optional[int]
    quota_limit: Optional[int]
    quota_used: int = 0


class RequestGetProviderModelList(BaseSchema):
    provider_id: constr(min_length=1)


class ResponseGetProviderModelList(BaseSchema):
    data: list[ModelWithProviderEntityResponse]


class RequestSaveModel(BaseSchema):
    provider: str
    model: str
    model_type: str
    credentials: dict
    load_balancing: Optional[ModelLoadBalanceConfig]


class ResponseSaveModel(BaseSchema):
    result: bool


class RequestChangeModelStatus(BaseSchema):
    model_type: str
    provider: str
    model: str
    status: bool


class ResponseChangeModelStatus(BaseSchema):
    result: bool


class RequestGetModelCredentials(BaseSchema):
    provider: str
    model_type: str
    model: str


class ResponseGetModelCredentials(BaseSchema):
    data: dict | None


class RequestDeleteModel(BaseSchema):
    provider: str
    model: str
    model_type: str


class ResponseDeleteModel(BaseSchema):
    result: bool


class ProviderWithModelsResponse(BaseSchema):
    tenant_uuid: str
    provider: str
    label: I18nObject
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    status: CustomConfigurationStatus
    models: list[ProviderModelWithStatusEntity]


class ResponseGetModelsByModelType(BaseSchema):
    data: list[ProviderWithModelsResponse]


class DefaultModelResponse(BaseModel):
    model: str
    model_type: ModelType
    provider: SimpleProviderEntityResponse

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())


class ResponseGetDefaultModelByModelType(BaseSchema):
    data: DefaultModelResponse | None


class UpdateDefaultModel(BaseSchema):
    model_type: str
    provider: Optional[str] = None
    model: Optional[str] = None


class RequestUpdateDefaultModels(BaseSchema):
    model_settings: list[UpdateDefaultModel]


class ResponseUpdateDefaultModels(BaseSchema):
    result: bool


class RequestGetModelParameterRule(BaseSchema):
    provider: str
    model: str


class ResponseGetModelParameterRule(BaseSchema):
    data: list[ParameterRule]
