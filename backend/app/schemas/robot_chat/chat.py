from typing import Optional

from app.schemas.robot_chat.conversation import MessageSchema
from app.schemas.base import BaseSchema


class RequestChat(BaseSchema):
    llm: str | None
    conversationUUID: Optional[str] | None
    appUUID: Optional[str] | None
    messages: list[MessageSchema]


class ResponseChatStream:
    data: str

    def __init__(self, data: str):
        super().__init__()
        self.data = data
