from pydantic import UUID4
from typing import Optional

from app.models import AppModelConfig
from app.schemas.base import BaseSchema


class AppModelConfigSchema(BaseSchema):
    app_uuid: Optional[UUID4] = None
    provider_uuid: Optional[UUID4] = None
    configs: Optional[str] = None
    persona_prompt: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: AppModelConfig):
        # print(type(obj), obj,super())
        # base = super().from_orm(obj)
        # print(type(base), **base.dict())
        return cls(
            # **base,
            app_uuid=obj.app_uuid,
            provider_uuid=obj.model_provider_uuid,
            configs=obj.configs,
            persona_prompt=obj.persona_prompt,
        )


class ResponseAppModelConfig(BaseSchema):
    app_model_config: AppModelConfigSchema
