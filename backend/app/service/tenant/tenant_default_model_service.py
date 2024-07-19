from typing import List, Tuple
from app.models.tenant.tenant import TenantDefaultModel
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.schemas.tenant.tenant import TenantDefaultModelSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class TenantDefaultModelService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_default_model_dao = TenantDefaultModelDAO(self.db)

    async def create_tenant_default_model(self, model_data: TenantDefaultModelSchema) -> Tuple[
        TenantDefaultModel | None, Exception]:
        try:
            return await self.tenant_default_model_dao.create_tenant_default_model(model_data)
        except SQLAlchemyError as e:
            return None, e

    async def get_tenant_default_models_by_uuid(self, tenant_uuid: str) -> Tuple[
        List[TenantDefaultModel] | None, Exception]:
        try:
            return await self.tenant_default_model_dao.get_tenant_default_model_by_uuid(tenant_uuid)
        except SQLAlchemyError as e:
            return None, e

    async def delete_tenant_default_model(self, tenant_uuid: str, provider_name: str, model_name: str) -> Tuple[
        bool, Exception]:
        try:
            return await self.tenant_default_model_dao.delete_tenant_default_model(tenant_uuid, provider_name, model_name)
        except SQLAlchemyError as e:
            return False, e
