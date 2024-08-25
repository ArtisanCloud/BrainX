from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.tenant.tenant import Tenant


class TenantDAO(BaseDAO[Tenant]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, Tenant)

    async def load_owner_user(self, tenant: Tenant):
        stmt = select(User).filter_by(tenant_owner_uuid=tenant.tenant_owner_uuid)
        result = await self.db.execute(stmt)
        tenant.owned_user = result.scalar_one_or_none()

        return tenant
