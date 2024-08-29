from typing import Union, Tuple, Optional

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
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
