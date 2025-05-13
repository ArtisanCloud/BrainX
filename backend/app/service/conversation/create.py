from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.robot_chat.conversation import ConversationSchema
from app.service.conversation.service import (
    ConversationService,
    transform_conversation_to_reply,
)

from app.models.robot_chat.conversation import Conversation


async def create_conversation(
   async_db: AsyncSession, conversation: Conversation
) -> Tuple[ConversationSchema | None, Exception | None]:
    service_conversation = ConversationService(async_db)

    conversation, exception = await service_conversation.create_conversation(
        conversation
    )

    if exception:
        return None, exception

    return transform_conversation_to_reply(conversation), None
