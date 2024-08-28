from typing import Union
from app.dao.base import BaseDAO
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant.tenant import TenantDefaultModel


class TenantDefaultModelDAO(BaseDAO[TenantDefaultModel]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, TenantDefaultModel)

    def get_default_model_by_uuid(self, tenant_uuid: str, model_type: str):
        return None
