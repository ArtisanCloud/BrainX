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
