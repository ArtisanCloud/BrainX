from pydantic import BaseModel


class JWT(BaseModel):
    jwt_secret: str
    expire_in: int


class Api(BaseModel):
    api_prefix: str
    openapi_prefix: str
    request_timeout: int
