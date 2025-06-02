import base64

from sqlalchemy.orm import Session

from app.core.libs import rsa
from app.core.libs.rsa import generate_key_pair
from app.dao.tenant.tenant import TenantDAO
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tenant


class TenantService:

    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.async_db = async_db
        self.sync_db = sync_db
        self.tenant_dao = TenantDAO(async_db=self.async_db, sync_db=self.sync_db)

    async def add_tenant(self, tenant: Tenant) -> Tenant:
        tenant.encrypted_public_key = generate_key_pair(tenant.uuid)

        tenant, exception = await self.tenant_dao.async_create(tenant)

        if exception:
            raise exception

        return tenant
