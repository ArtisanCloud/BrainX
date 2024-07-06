from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.app import App
from app.models.robot_chat.conversation import Conversation


class ConversationDAO(BaseDAO[Conversation]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Conversation)
