from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.robot_chat.conversation import Conversation


class ConversationDAO(BaseDAO[Conversation]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, Conversation)
