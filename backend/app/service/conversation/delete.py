from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.conversation.service import ConversationService


async def soft_delete_conversation(
        db: AsyncSession,
        user_id: int,
        conversation_uuid: str
) -> Tuple[bool | None, Exception | None]:
    service_conversation = ConversationService(db)
    result, exception = await service_conversation.soft_delete_conversation(user_id, conversation_uuid)

    if exception:
        return False, exception

    return result, None
