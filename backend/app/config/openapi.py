from pydantic import BaseModel

from app.config.openapi_provider.powerx import PowerX as PowerXProvider
from app.config.openapi_platofrm.powerx import PowerX as PowerXPlatform


class OpenAPIProvider(BaseModel):
    power_x: PowerXProvider


class OpenAPIPlatform(BaseModel):
    token_secret_key: str
    power_x: PowerXPlatform


class OpenAPI(BaseModel):
    platforms: OpenAPIPlatform
    providers: OpenAPIProvider
