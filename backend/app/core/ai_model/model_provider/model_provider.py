from abc import ABC
from typing import List, Dict, Any

from app.core.ai_model.model_instance import ModelInstance
from app.core.ai_model.model_provider.schema.provider import ProviderSchema


class ModelProvider(ABC):
    def __init__(self, name: str, config: dict):
        # 初始化提供商
        self.config = config
        self.provider_schema: ProviderSchema | None = None
        self.dict_provider_model = Dict[str, Any]

    def verify_provider_credentials(self, credentials: dict) -> Exception:
        raise NotImplementedError("This method should be implemented by subclasses")
