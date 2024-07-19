from typing import Tuple
from app.models.tenant.tenant import Tenant
from app.dao.tenant.tenant import TenantDAO
from app.schemas.tenant.tenant import TenantSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class TenantService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_dao = TenantDAO(self.db)

    async def create_tenant(self, tenant_data: TenantSchema) -> Tuple[Tenant | None, Exception]:
        try:
            return await self.tenant_dao.create_tenant(tenant_data)
        except SQLAlchemyError as e:
            return None, e

    async def get_tenant_by_name(self, name: str) -> Tuple[Tenant | None, Exception]:
        try:
            return await self.tenant_dao.get_tenant_by_name(name)
        except SQLAlchemyError as e:
            return None, e

    async def update_tenant(self, name: str, tenant_data: TenantSchema) -> Tuple[Tenant | None, Exception]:
        try:
            return await self.tenant_dao.update_tenant(name, tenant_data)
        except SQLAlchemyError as e:
            return None, e

    async def delete_tenant(self, name: str) -> Tuple[bool, Exception]:
        try:
            return await self.tenant_dao.delete_tenant(name)
        except SQLAlchemyError as e:
            return False, e
