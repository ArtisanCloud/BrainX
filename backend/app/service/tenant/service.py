from app.dao.tenant.tenant import TenantDAO
from sqlalchemy.ext.asyncio import AsyncSession


class TenantService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_dao = TenantDAO(self.db)
