from typing import Union, Tuple, Optional, List

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant.provider_config import provider_config
from app.dao.base import BaseDAO
from app.models import Provider, User
from app.models.tenant.tenant import TenantDefaultModel


class TenantDefaultModelDAO(BaseDAO[TenantDefaultModel]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, TenantDefaultModel)

    async def async_get_default_model_by_uuid(self, tenant_uuid: str, model_type: str) -> Tuple[
        Optional[TenantDefaultModel], Optional[SQLAlchemyError]]:
        try:
            # print(tenant_uuid, model_type)
            query = self._get_default_model_by_uuid(tenant_uuid, model_type)
            # print("Generated SQL (async):", str(query))
            # 这里需要根据 db 类型执行查询操作
            result = await self.db.execute(query)
            default_model = result.scalars().first()

            return default_model, None

        except SQLAlchemyError as e:
            return None, e

    def get_default_model_by_uuid(self, tenant_uuid: str, model_type: str) -> Tuple[
        Optional[TenantDefaultModel], Optional[SQLAlchemyError]]:
        try:
            query = self._get_default_model_by_uuid(tenant_uuid, model_type)
            print(query, tenant_uuid, model_type)
            # 这里需要根据 db 类型执行查询操作
            result = self.db.execute(query)  # 同步查询
            default_model = result.scalars().first()
            return default_model, None

        except SQLAlchemyError as e:

            return None, e

    def _get_default_model_by_uuid(self, tenant_uuid: str, model_type: str):
        query = (
            select(TenantDefaultModel)
            .filter(
                and_(
                    TenantDefaultModel.tenant_uuid == tenant_uuid,
                    TenantDefaultModel.type == model_type
                )
            )
        )

        return query

    async def get_tenant_default_model_from_config(self, user: User) -> Tuple[
        List[TenantDefaultModel] | None, Exception | None]:
        try:
            result = await self.db.execute(select(Provider))
            providers = result.scalars().all()  # 获取结果列表
            # print(providers)
            models = []
            for provider in providers:
                for model_name, model_configs in provider_config[provider.provider_name]["models"].items():
                    model = TenantDefaultModel(
                        tenant_uuid=user.tenant_owner_uuid,
                        provider_uuid=provider.uuid,
                        provider_name=provider.provider_name,
                        name=model_name,
                        type=model_configs["type"],
                    )
                    models.append(model)
            return models, None

        except Exception as e:
            return None, e