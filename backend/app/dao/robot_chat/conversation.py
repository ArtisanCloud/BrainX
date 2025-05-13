from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.robot_chat.conversation import Conversation


class ConversationDAO(BaseDAO[Conversation]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Conversation, async_db, sync_db)
