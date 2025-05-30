from enum import Enum
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.constant.ai_model.provider import ProviderID
from app.core.brainx.model_instance import ModelInstance
from app.core.brainx.provider_manager import ProviderManager
from app.models.model_provider.provider_model import ModelType


class ModelManager:
    provider_manager: ProviderManager
    provider_id: str = None
    model_id: str = None

    def __init__(self,
                 async_db: AsyncSession = None, sync_db: Session = None,
                 provider_id=None, model_id=None,
                 ):
        self.provider_manager = ProviderManager(
            async_db=async_db, sync_db=sync_db,
            provider_id=provider_id, model_id=model_id
        )
        self.provider_id = provider_id
        self.model_id = model_id

    def get_default_provider_model_name(self, tenant_uuid: str, model_type: ModelType) -> tuple[str | None, str | None]:
        return self.provider_manager.get_first_provider_first_model(tenant_uuid, model_type)

    def get_model_instance(
            self,
            tenant_uuid: str, model_type: ModelType,
            provider_id: str, model_id: str
    ) -> Tuple[Optional[ModelInstance], Optional[Exception]]:

        # print(3330000, model_type, provider, model)
        # 重载provider和model
        if model_type == ModelType.LLM:
            if self.provider_id is not None:
                provider_id = self.provider_id
            if self.model_id is not None:
                model_id = self.model_id
        print(33333333, provider_id, model_id)

        # 如果没有提供provider名称
        if not provider_id:
            return self.get_default_model_instance(tenant_uuid, model_type)

        # 获取指定租户的provider模型
        model_bundle, exception = self.provider_manager.get_provider_model_bundle(
            tenant_uuid, model_type, provider_id, model_id,
        )
        if exception is not None:
            return None, exception

        return ModelInstance(
            model_bundle=model_bundle,
            model=model_id,
        ), None

    def get_default_model_instance(
            self, tenant_uuid: str, model_type: ModelType
    ) -> Tuple[Optional[ModelInstance], Optional[Exception]]:

        # 获取默认模型
        default_model_record, exception = self.provider_manager.get_default_model(tenant_uuid, model_type)
        if exception is not None:
            return None, exception

        if not default_model_record:
            raise Exception(f"Default model not found for {model_type}")

        # 获取默认模型实例
        return self.get_model_instance(
            tenant_uuid=tenant_uuid,
            model_type=model_type,
            provider_id=default_model_record.provider_name,
            model_id=default_model_record.name,
        )

    @classmethod
    def generate_model_id(cls, provider_id: ProviderID, model_enum: Enum) -> str:
        """
        将 provider_id 和 model_provider name 组合生成唯一的 model_id。
        """
        return f"{provider_id.value}.{model_enum.value}"
