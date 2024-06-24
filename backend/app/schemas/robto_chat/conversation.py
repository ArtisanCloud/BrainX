from app.schemas.base import BaseSchema


class Message(BaseSchema):
    content: str | None
    role: str | None
