from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.core.brainx.drivers.provider_model_factory import ProviderModelFactory
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.interface.ai_model import AIModel


class ProviderInterface(BaseModel):
    tenant_uuid: str
    provider_id: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def validate_credentials(
            self,
            tenant_uuid: str,
            user_uuid: str,
            provider_id: str,
            credentials: dict,
            model_type: str = None,
            model_id: str = None,
    ) -> Optional[Exception]:
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_model_type_instance(self, model_type: ModelType, model_id: str) -> AIModel:
        model_provider_factory = ProviderModelFactory(self.tenant_uuid)

        return model_provider_factory.get_model_type_instance(
            model_type=model_type,
            provider_id=self.provider_id,
            model_id=model_id,
        )
