from pydantic import BaseModel, UUID4, constr, AnyHttpUrl
from typing import Optional


class AppModelConfigSchema(BaseModel):
    app_uuid: UUID4
    model_provider_uuid: UUID4
    configs: Optional[str]
    persona_prompt: Optional[str]


class ResponseAppModelConfig(BaseModel):
    app_model_config: AppModelConfigSchema
