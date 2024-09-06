from app.schemas.auth import AccessTokenSchema
from app.schemas.base import BaseSchema


class RequestAuthPlatform(BaseSchema):
    platform: str
    access_key: str
    secret_key: str


class ResponseAuthPlatform(BaseSchema):
    platform: str
    token: AccessTokenSchema
