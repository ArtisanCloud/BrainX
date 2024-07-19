from pydantic import BaseModel


class TenantSchema(BaseModel):
    name: str
    plan: int
    status: int
    encrypted_public_key: str
    config: str


class TenantDefaultModelSchema(BaseModel):
    tenant_uuid: str
    provider_name: str
    name: str
    type: str
