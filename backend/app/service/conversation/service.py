from typing import Tuple, Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.conversation import ConversationDAO
from app.models.robot_chat.conversation import Conversation


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.conversation_dao = ConversationDAO(db)
    #
    # async def create_conversations(self, conversations_data: List[Dict[str, Any]]) -> Tuple[List[Conversation] | None, Exception | None]:
    #     try:
    #         conversations = [Conversation(**data) for data in conversations_data]
    #         created_conversations = await self.conversation_dao.create_many(conversations)
    #         return created_conversations, None
    #     except SQLAlchemyError as e:
    #         return None, e
    #
    # async def patch_conversation(self, conversation_uuid: str, update_data: Dict[str, Any]) -> Tuple[Conversation | None, Exception | None]:
    #     try:
    #         updated_conversation = await self.conversation_dao.patch(conversation_uuid, update_data)
    #         return updated_conversation, None
    #     except SQLAlchemyError as e:
    #         return None, e
    #
    # async def get_conversation_by_uuid(self, conversation_uuid: str) -> Tuple[Conversation | None, Exception | None]:
    #     try:
    #         conversation = await self.conversation_dao.get_by_uuid(conversation_uuid)
    #         return conversation, None
    #     except SQLAlchemyError as e:
    #         return None, e
    #
    # async def soft_delete_conversation(self, user_id: int, conversation_uuid: str) -> Tuple[bool, Exception | None]:
    #     try:
    #         success, error = await self.conversation_dao.soft_delete(user_id, conversation_uuid)
    #         return success, error
    #     except SQLAlchemyError as e:
    #         return False, e
    #
    # async def delete_conversation(self, user_id: int, conversation_uuid: str) -> Tuple[bool, Exception | None]:
    #     try:
    #         success, error = await self.conversation_dao.delete(user_id, conversation_uuid)
    #         return success, error
    #     except SQLAlchemyError as e:
    #         return False, e
