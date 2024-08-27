from typing import List

from sqlalchemy.orm import Session

from app.core.ai_model.model_instance import ModelInstance
from app.core.ai_model.model_provider.provider_manager import ProviderManager
from app.models import ProviderModel
from app.models.model_provider.provider_model import ModelType


class ModelManager:
    def __init__(self):
        # 初始化模型管理器
        self._provider_manager = ProviderManager()

    def get_default_model_instance(
            self, db: Session,
            tenant_uuid: str, model_type: ModelType
    ) -> ModelInstance:



        # 获取默认模型实例
        return ModelInstance(
            tenant_uuid=tenant_uuid,
            model_type=model_type,
        )
