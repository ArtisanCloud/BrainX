from typing import Tuple, Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.conversation import ConversationDAO
from app.models.robot_chat.conversation import Conversation


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.conversation_dao = ConversationDAO(db)
   