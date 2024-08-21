from app.schemas.base import BaseSchema


class TenantSchema(BaseSchema):
    name: str
    plan: int
    status: int
    encrypted_public_key: str
    config: str


class TenantDefaultModelSchema(BaseSchema):
    tenant_uuid: str
    provider_name: str
    name: str
    type: str
