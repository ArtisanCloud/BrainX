from pydantic import BaseModel, UUID4, constr, AnyHttpUrl
from typing import Optional

from app.schemas.base import BaseSchema


class AppModelConfigSchema(BaseSchema):
    app_uuid: UUID4
    model_provider_uuid: UUID4
    configs: Optional[str]
    persona_prompt: Optional[str]


class ResponseAppModelConfig(BaseSchema):
    app_model_config: AppModelConfigSchema
