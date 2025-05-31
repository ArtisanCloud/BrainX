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

    def encrypt_content(self, tenant_uuid: str, content: str):
        tenant, exception = self.tenant_dao.sync_get_by_uuid(tenant_uuid)
        if exception:
            raise exception
        if not tenant:
            raise ValueError(f"Tenant with uuid {tenant_uuid} not found")

        encrypted_content = rsa.rsa_encrypt(tenant.encrypted_public_key, content)

        return base64.b64encode(encrypted_content).decode()

    def decrypt_content(self, tenant_uuid: str, content: str) -> str:

        private_key_path = rsa.get_tenant_private_key_path(tenant_uuid)
        return rsa.rsa_decrypt(private_key_path, base64.b64decode(content))
