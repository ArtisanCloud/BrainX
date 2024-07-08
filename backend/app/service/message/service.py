from langchain_core.messages import BaseMessage

from app.dao.message import MessageDAO

from typing import Optional, Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.robot_chat.conversation import Message
from app.schemas.base import Pagination, ResponsePagination


class MessageService:
    def __init__(self, db: AsyncSession):
        self.conversation_dao = MessageDAO(db)

    async def get_cached_message_list(self, conversation_uuid: str, p: Pagination) -> Tuple[
        Optional[List[BaseMessage]], Optional[ResponsePagination], Optional[Exception]]:
        messages, exception = await self.conversation_dao.get_cached_message_list(conversation_uuid, p)

        return messages, ResponsePagination(
            limit=0,
            page=0,
            sort=0,
            total_rows=0,
            total_pages=0,
        ), exception
