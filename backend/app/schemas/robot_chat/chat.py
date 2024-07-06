from app.schemas.robot_chat.conversation import MessageSchema
from app.schemas.base import BaseSchema


class RequestChat(BaseSchema):
    llm: str | None
    conversationUUID: str | None
    appUUID: str | None
    messages: list[MessageSchema]


class ResponseChatStream:
    data: str

    def __init__(self, data: str):
        super().__init__()
        self.data = data
