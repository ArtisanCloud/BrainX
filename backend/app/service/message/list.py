from typing import Tuple, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.robot_chat.conversation import MessageSchema

from app.service.base import paginate_query

from app.models.robot_chat.conversation import Message
from app.service.message.service import (
    MessageService,
    transform_cached_messages_to_reply,
    transform_messages_to_reply,
)


async def get_cached_message_list(
   async_db: AsyncSession,
    conversation_uuid: str,
    pagination: Pagination,
) -> Tuple[
    List[MessageSchema] | None, ResponsePagination | None, SQLAlchemyError | None
]:
    service_message = MessageService(async_db)
    messages, pg, exception = await service_message.get_cached_message_list(
        conversation_uuid, pagination
    )

    # print(res, pg, exception)
    if exception:
        return None, None, exception

    return transform_cached_messages_to_reply(messages), pg, None


async def get_message_list(
   async_db: AsyncSession, pagination: Pagination, app_uuid: str | None = None
) -> Tuple[
    List[MessageSchema] | None, ResponsePagination | None, SQLAlchemyError | None
]:
    stmt = (
        select(Message)
        .where(Message.deleted_at.is_(None))
        .where(Message.app_uuid == app_uuid)
        .order_by(desc(Message.updated_at))
    )
    # print(stmt)
    res, pg, exception = await paginate_query(async_db, stmt, Message, pagination, True)
    # print(res, pg, exception)
    if exception:
        return None, None, exception

    return transform_messages_to_reply(res), pg, None
