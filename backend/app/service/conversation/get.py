from sqlalchemy.ext.asyncio import AsyncSession

from app.models.robot_chat.conversation import Conversation


async def get_conversation_by_id(
        db: AsyncSession,
        conversation_id: int
) -> Conversation:
    return await db.get(Conversation, conversation_id)
