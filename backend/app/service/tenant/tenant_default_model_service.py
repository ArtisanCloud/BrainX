from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from sqlalchemy.ext.asyncio import AsyncSession


class TenantDefaultModelService:
    def __init__(self,async_db: AsyncSession):
        self.async_db = async_db
        self.tenant_default_model_dao = TenantDefaultModelDAO(self.async_db)
