from typing import Type, Optional, Tuple, List

from langchain_core.messages import BaseMessage
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.robot_chat.conversation import Message
from app.schemas.base import Pagination
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory

from app.schemas.robot_chat.conversation import MessageSchema


class MessageDAO(BaseDAO[Message]):
    def __init__(self,
                 db: AsyncSession,
                 chat_history_cls: Type[ChatMessageHistory] = RedisChatMessageHistory
                 ):
        super().__init__(db, Message)

        self.cached_chat_history_cls = chat_history_cls
        self.chat_history_kwargs = {}

    def get_chat_history(self, session_id: str) -> ChatMessageHistory:
        return self.cached_chat_history_cls(session_id=session_id, **self.chat_history_kwargs)

    async def get_cached_message_list(self, conversation_uuid: str, p: Pagination) -> Tuple[
        Optional[List[BaseMessage]], Optional[Exception]]:
        chat_history_handler = self.get_chat_history(session_id=conversation_uuid)
        messages = chat_history_handler.messages
        # print("message:", messages)

        return messages, None
