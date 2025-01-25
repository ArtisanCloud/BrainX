from typing import List, Optional

from app.schemas.robot_chat.conversation import MessageSchema
from app.schemas.base import BaseSchema


class RequestChat(BaseSchema):
    llm: str | None
    conversationUUID: Optional[str] | None
    appUUID: Optional[str] | None
    messages: list[MessageSchema]
    images: Optional[List[str]] = None


class RequestCompletion(BaseSchema):
    llm: str | None
    appUUID: Optional[str] | None
    system: Optional[str] | None
    user: Optional[str] | None
    messages: Optional[list[MessageSchema]] | None = None
    images: Optional[List[str]] = None


class ResponseChatCompletion(BaseSchema):
    data: str
