from app.schemas.robto_chat.conversation import Message
from app.schemas.base import BaseSchema


class RequestChat(BaseSchema):
    llm: str | None
    conversationUUID: str | None
    messages: list[Message]


class ResponseChatStream:
    data: str

    def __init__(self, data: str):
        super().__init__()
        self.data = data
