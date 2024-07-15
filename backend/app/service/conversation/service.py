from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.robot_chat.conversation import ConversationDAO


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.conversation_dao = ConversationDAO(db)
   