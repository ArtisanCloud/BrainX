from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.app.app import App


class AppDAO(BaseDAO[App]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, App)
