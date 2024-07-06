from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.robot_chat.conversation import ConversationSchema
from app.service.conversation.create import transform_conversation_to_reply
from app.service.conversation.service import ConversationService


async def patch_conversation(
        db: AsyncSession,
        conversation_uuid: str,
        update_data: Dict[str, Any]
) -> Tuple[ConversationSchema | None, Exception | None]:
    service_conversation = ConversationService(db)
    conversation, exception = await service_conversation.patch_conversation(conversation_uuid, update_data)

    if exception:
        return None, exception

    return transform_conversation_to_reply(conversation), None
