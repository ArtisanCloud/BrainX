from enum import Enum
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.model_instance import ModelInstance
from app.core.ai_model.provider_manager import ProviderManager
from app.core.rag import FrameworkDriverType
from app.models.model_provider.provider_model import ModelType


class ModelManager:
    def __init__(self, framework_type: FrameworkDriverType):
        # 初始化模型管理器
        # 提供底层的提供商管理功能
        self.provider_manager = ProviderManager(framework_type)

    def get_model_instance(self, db: Session, tenant_uuid: str, provider: str, model_type: ModelType) -> Tuple[
        Optional[ModelInstance], Optional[Exception]]:
        if not provider:
            return self.get_default_model_instance(db, tenant_uuid, model_type)

        model, exception = self.provider_manager.get_model(
            db, tenant_uuid,
            provider, model_type
        )
        if exception is not None:
            return None, exception

        return ModelInstance(
            model=model,
            config={},
        ), None

    def get_default_model_instance(
            self, db: Session, tenant_uuid: str, model_type: ModelType
    ) -> Tuple[Optional[ModelInstance], Optional[Exception]]:

        model, exception = self.provider_manager.get_default_model(db, tenant_uuid, model_type)
        if exception is not None:
            return None, exception

        # 获取默认模型实例
        return ModelInstance(
            model=model,
            config={},
        ), None

    @classmethod
    def generate_model_id(cls, provider_id: ProviderID, model_enum: Enum) -> str:
        """
        将 provider_id 和 model_provider name 组合生成唯一的 model_id。
        """
        return f"{provider_id.value}.{model_enum.value}"
