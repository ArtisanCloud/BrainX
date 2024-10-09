from typing import Optional, Any

from app.schemas.base import BaseSchema


class RequestDemoQuery(BaseSchema):
    llm: Optional[str | None] = None
    question: str


class ResponseDemoQuery(BaseSchema):
    data: Any


class DemoStructuredUserInfo(BaseSchema):
    name: str
    age: int
    profession: str
