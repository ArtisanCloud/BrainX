import json
from typing import Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.provider_manager import ProviderManager
from app.dao.model_provider.provider_model import ProviderModelDAO
from app.models import ProviderModel
from app.schemas.model_provider.provider import ModelWithProviderEntityResponse
from app.schemas.model_provider.provider_model import ProviderModelSchema
from app.utils.cache.provider_credentials import ProviderCredentialsCache, ProviderCredentialsCacheType


class ProviderModelService:
    async_db: AsyncSession
    sync_db: Session
    provider_model_dao: ProviderModelDAO

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.provider_model_dao = ProviderModelDAO(async_db=async_db, sync_db=sync_db)
        self.sync_db = sync_db
        self.async_db = async_db

    def get_models_by_provider(self, tenant_uuid: str, provider_id: str) -> List[ModelWithProviderEntityResponse]:
        provider_manager = ProviderManager(sync_db=self.sync_db)
        configurations = provider_manager.get_configurations(tenant_uuid)

        all_models = configurations.get_models(provider=provider_id)
        models = []
    
        for provider_model in all_models:
            models.append(ModelWithProviderEntityResponse(
                tenant_uuid=tenant_uuid,
                provider_model=provider_model
            ))
        return models

    def save_model_credentials(
            self, tenant_uuid: str, model_type: ModelType,
            provider: str, model: str, credentials: dict
    ) -> Tuple[ProviderModelSchema | None, Exception | None]:
        try:
            provider_manager = ProviderManager(sync_db=self.sync_db)
            provider_model_service = ProviderModelService(sync_db=self.sync_db)

            # 加载租户的模型配置表
            configurations = provider_manager.get_configurations(tenant_uuid)

            # 获取指定的provider配置
            provider_configuration = configurations.get(provider)
            if provider_configuration is None:
                raise Exception(f"Cannot find provider configuration for {provider}")

            # 验证 credentials 是否有效
            provider_model_record, credentials = provider_configuration.validate_provider_model_credentials(
                model_type=model_type, model=model, credentials=credentials
            )
            # print(provider_model_record, credentials)

            if provider_model_record:
                dict_provider_model_record: dict = {}
                dict_provider_model_record["encrypted_config"] = json.dumps(credentials)
                dict_provider_model_record["is_valid"] = True
                provider_model_record, exception = provider_model_service.provider_model_dao.sync_update(
                    provider_model_record.uuid, dict_provider_model_record
                )
            else:
                provider_model_record = ProviderModel()
                provider_model_record.tenant_uuid = tenant_uuid
                provider_model_record.provider_name = provider
                provider_model_record.model_name = model
                provider_model_record.model_type = model_type.value
                provider_model_record.encrypted_config = json.dumps(credentials)
                provider_model_record.is_valid = True
                provider_model_record, exception = provider_model_service.provider_model_dao.sync_create(
                    provider_model_record
                )

            if exception:
                raise exception

            provider_model_credentials_cache = ProviderCredentialsCache(
                tenant_uuid=tenant_uuid,
                identity_id=provider_model_record.uuid,
                cache_type=ProviderCredentialsCacheType.MODEL,
            )
            provider_model_credentials_cache.delete()

            if exception:
                raise exception

        except Exception as e:
            return None, e

        return provider_model_record, None
