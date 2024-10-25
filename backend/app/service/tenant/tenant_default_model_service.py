from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from sqlalchemy.ext.asyncio import AsyncSession


class TenantDefaultModelService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_default_model_dao = TenantDefaultModelDAO(self.db)
