from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.robot_chat.conversation import ConversationDAO
from app.models.robot_chat.conversation import Conversation
from app.schemas.robot_chat.conversation import ConversationSchema


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.conversation_dao = ConversationDAO(db)


def transform_conversation_to_reply(
    conversation: Conversation,
) -> [ConversationSchema | None]:
    if conversation is None:
        return None

    return ConversationSchema.from_orm(conversation)


def transform_conversations_to_reply(
    conversations: [Conversation],
) -> List[ConversationSchema]:
    data = [transform_conversation_to_reply(resource) for resource in conversations]
    # print(data)
    return data
