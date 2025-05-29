from enum import Enum
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.constant.ai_model.provider import ProviderID
from app.core.brainx.model_instance import ModelInstance
from app.core.brainx.provider_manager import ProviderManager
from app.core.rag import FrameworkDriverType
from app.models.model_provider.provider_model import ModelType


class ModelManager:
    provider_manager: ProviderManager

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.provider_manager = ProviderManager(async_db=async_db, sync_db=sync_db)

    def get_default_provider_model_name(self, tenant_uuid: str, model_type: ModelType) -> tuple[str | None, str | None]:
        return self.provider_manager.get_first_provider_first_model(tenant_uuid, model_type)

    def get_model_instance(
            self,
            tenant_uuid: str, provider: str, model_type: ModelType, model: str
    ) -> Tuple[Optional[ModelInstance], Optional[Exception]]:

        # 如果没有提供provider名称
        if not provider:
            return self.get_default_model_instance(tenant_uuid, model_type)

        # 获取指定租户的provider模型
        model_bundle, exception = self.provider_manager.get_provider_model_bundle(
            tenant_uuid, provider, model_type
        )
        if exception is not None:
            return None, exception

        return ModelInstance(
            model_bundle=model_bundle,
            model=model,
        ), None

    def get_default_model_instance(
            self, tenant_uuid: str, model_type: ModelType
    ) -> Tuple[Optional[ModelInstance], Optional[Exception]]:

        default_model_record, exception = self.provider_manager.get_default_model(tenant_uuid, model_type)
        if exception is not None:
            return None, exception

        if not default_model_record:
            raise Exception(f"Default model not found for {model_type}")

        # 获取默认模型实例
        return self.get_model_instance(
            tenant_uuid=tenant_uuid,
            provider=default_model_record.provider_name,
            model_type=model_type,
            model=default_model_record.name,
        )

    @classmethod
    def generate_model_id(cls, provider_id: ProviderID, model_enum: Enum) -> str:
        """
        将 provider_id 和 model_provider name 组合生成唯一的 model_id。
        """
        return f"{provider_id.value}.{model_enum.value}"
