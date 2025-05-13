from app.dao.tenant.tenant import TenantDAO
from sqlalchemy.ext.asyncio import AsyncSession


class TenantService:
    def __init__(self,async_db: AsyncSession):
        self.async_db = async_db
        self.tenant_dao = TenantDAO(self.async_db)
