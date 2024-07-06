from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.robot_chat.conversation import ConversationSchema
from app.service.conversation.service import ConversationService

from app.models.robot_chat.conversation import Conversation


def transform_conversation_to_reply(conversation: Conversation) -> [ConversationSchema | None]:
    if conversation is None:
        return None

    return ConversationSchema.from_orm(conversation)


async def create_conversation(
        db: AsyncSession,
        conversation: Conversation
) -> Tuple[ConversationSchema | None, Exception | None]:
    service_conversation = ConversationService(db)

    conversation, exception = await service_conversation.create_conversation(conversation)

    if exception:
        return None, exception

    return transform_conversation_to_reply(conversation), None
