from sqlalchemy.ext.asyncio import AsyncSession

from app.models.robot_chat.conversation import Conversation


async def get_conversation_by_id(
        async_db: AsyncSession,
        conversation_id: int
) -> Conversation:
    conversation, err = await async_db.get(Conversation, conversation_id)
    return conversation
