from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.robot_chat.conversation import MessageSchema
from app.service.message.service import MessageService, transform_message_to_reply

from app.models.robot_chat.conversation import Message


async def create_message(
   async_db: AsyncSession, message: Message
) -> Tuple[MessageSchema | None, Exception | None]:
    service_message = MessageService(async_db)

    message, exception = await service_message.create_message(message)

    if exception:
        return None, exception

    return transform_message_to_reply(message), None
