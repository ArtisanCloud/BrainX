from langchain_core.messages import BaseMessage

from app.dao.robot_chat.message import MessageDAO

from typing import Optional, Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.robot_chat.conversation import Message
from app.schemas.base import Pagination, ResponsePagination
from app.schemas.robot_chat.conversation import MessageSchema


class MessageService:
    def __init__(self, async_db: AsyncSession):
        self.conversation_dao = MessageDAO(async_db)

    async def get_cached_message_list(
            self, conversation_uuid: str, p: Pagination
    ) -> Tuple[
        Optional[List[BaseMessage]], Optional[ResponsePagination], Optional[Exception]
    ]:
        messages, exception = await self.conversation_dao.get_cached_message_list(
            conversation_uuid, p
        )

        return (
            messages,
            ResponsePagination(
                limit=0,
                page=0,
                sort=0,
                total_rows=0,
                total_pages=0,
            ),
            exception,
        )


def transform_message_to_reply(message: Message) -> [MessageSchema | None]:
    if message is None:
        return None

    return MessageSchema.from_orm(message)


def transform_messages_to_reply(messages: [Message]) -> List[MessageSchema]:
    data = [transform_message_to_reply(message) for message in messages]
    # print(data)
    return data


def transform_cached_messages_to_reply(messages: [BaseMessage]) -> List[MessageSchema]:
    data = [transform_cached_message_to_reply(message) for message in messages]
    # print(data)
    return data


def transform_cached_message_to_reply(message: BaseMessage) -> [MessageSchema | None]:
    if message is None:
        return None

    return MessageSchema(content=message.content, type=message.type)
