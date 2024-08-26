from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.model_provider.provider_model import ProviderModel
from app.dao.base import BaseDAO


class ProviderModelDAO(BaseDAO[ProviderModel]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, ProviderModel)
