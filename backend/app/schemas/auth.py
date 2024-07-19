from app import settings
from app.schemas.base import BaseSchema
from app.schemas.tenant.user import UserSchema

token_expired_duration = 60 * 60 * 24 * 3
access_token_type = "Bearer"
auth_tenant_uuid_key = "tenant_uuid"
auth_user_uuid_key = "user_uuid"

SECRET_KEY = settings.jwt.jwt_secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AccessTokenSchema(BaseSchema):
    token_type: str
    expires_in: int = 7200
    access_token: str
    refresh_token: str


class RequestRegisterUser(BaseSchema):
    account: str
    password: str


class ResponseRegisterUser(BaseSchema):
    user: UserSchema


class RequestLoginUser(BaseSchema):
    account: str
    password: str


class ResponseLoginUser(BaseSchema):
    account: str
    token: AccessTokenSchema
