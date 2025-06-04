from typing import Optional
from pydantic import UUID4, constr
from datetime import datetime

from app.schemas.base import BaseSchema
from app.schemas.model_provider.load_balance import ModelLoadBalanceConfig
from app.schemas.model_provider.provider import ModelWithProviderEntityResponse


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
    success: bool
