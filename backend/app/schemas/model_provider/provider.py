from typing import Dict, Optional
from pydantic import UUID4, constr
from datetime import datetime
from app.core.ai_model.schema.provider import ProviderSchema

from app.schemas.base import BaseSchema


class ProvderSchema(BaseSchema):
    tenant_uuid: UUID4
    provider_name: constr(min_length=1)
    provider_type: constr(min_length=1)
    encrypted_config: Optional[str]
    is_valid: bool = False
    last_used: Optional[datetime]
    quota_type: Optional[int]
    quota_limit: Optional[int]
    quota_used: int = 0


class ResponseGetModelProviderList(BaseSchema):
    data: Dict[str, ProviderSchema]


class RequestCreateModelProvider(BaseSchema):
    name: constr(min_length=1)
    description: constr(min_length=1)


class ResponseCreateModelProvider(BaseSchema):
    result: bool
