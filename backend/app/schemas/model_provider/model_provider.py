from typing import Optional
from pydantic import UUID4, constr
from datetime import datetime

from app.schemas.base import BaseSchema


class ModelProviderSchema(BaseSchema):
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
