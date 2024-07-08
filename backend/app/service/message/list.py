import uuid
from typing import Tuple, List

from langchain_core.messages import BaseMessage
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UUID, desc

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.robot_chat.conversation import MessageSchema

from app.service.base import paginate_query
from app.service.message.create import transform_message_to_reply, transform_cached_message_to_reply

from app.models.robot_chat.conversation import Message
from app.service.message.service import MessageService


def transform_messages_to_reply(messages: [Message]) -> List[MessageSchema]:
    data = [transform_message_to_reply(message) for message in messages]
    # print(data)
    return data


def transform_cached_messages_to_reply(messages: [BaseMessage]) -> List[MessageSchema]:
    data = [transform_cached_message_to_reply(message) for message in messages]
    # print(data)
    return data


async def get_cached_message_list(
        db: AsyncSession,
        conversation_uuid: str,
        pagination: Pagination,
) -> Tuple[List[MessageSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    message_service = MessageService(db)
    messages, pg, exception = await message_service.get_cached_message_list(conversation_uuid, pagination)

    # print(res, pg, exception)
    if exception:
        return None, None, exception

    return transform_cached_messages_to_reply(messages), pg, None


async def get_message_list(
        db: AsyncSession,
        pagination: Pagination,
        app_uuid: str | None = None
) -> Tuple[List[MessageSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(Message).
        where(Message.deleted_at.is_(None)).
        where(Message.app_uuid == app_uuid).
        order_by(desc(Message.updated_at))
    )
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, Message, pagination, True)
    # print(res, pg, exception)
    if exception:
        return None, None, exception

    return transform_messages_to_reply(res), pg, None
