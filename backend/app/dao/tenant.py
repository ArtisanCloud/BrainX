from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.tenant import Tenant
from typing import List, Tuple
from app.schemas.tenant import TenantSchema


class TenantDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tenant(self, tenant_data: TenantSchema) -> Tuple[Tenant | None, Exception]:
        try:
            tenant = Tenant(**tenant_data.dict())
            self.db.add(tenant)
            await self.db.commit()
            return tenant, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def get_tenant_by_name(self, name: str) -> Tuple[Tenant | None, Exception | None]:
        try:
            stmt = select(Tenant).filter(Tenant.name == name)
            result = await self.db.execute(stmt)
            tenant = result.scalar_one_or_none()
            return tenant, None
        except SQLAlchemyError as e:
            return None, e

    async def update_tenant(self, name: str, tenant_data: TenantSchema) -> Tuple[Tenant | None, Exception]:
        try:
            tenant, error = await self.get_tenant_by_name(name)
            if error:
                return None, error

            if not tenant:
                return None, Exception(f"Tenant with name {name} not found")

            for field, value in tenant_data.dict(exclude_unset=True).items():
                setattr(tenant, field, value)

            await self.db.commit()
            return tenant, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def patch_tenant(self, name: str, patch_data: dict) -> Tuple[Tenant | None, Exception]:
        try:
            tenant, error = await self.get_tenant_by_name(name)
            if error:
                return None, error

            if not tenant:
                return None, Exception(f"Tenant with name {name} not found")

            for field, value in patch_data.items():
                if hasattr(tenant, field):
                    setattr(tenant, field, value)
                else:
                    return None, Exception(f"Invalid field '{field}' provided for patching")

            await self.db.commit()
            return tenant, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def delete_tenant(self, name: str) -> Tuple[bool, Exception]:
        try:
            tenant, error = await self.get_tenant_by_name(name)
            if error:
                return False, error

            if not tenant:
                return False, Exception(f"Tenant with name {name} not found")

            self.db.delete(tenant)
            await self.db.commit()
            return True, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return False, e
