from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.openapi.models.platform import Platform


class PlatformDAO(BaseDAO[Platform]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, Platform)