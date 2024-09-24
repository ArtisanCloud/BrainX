from typing import Optional

from app.schemas.base import BaseSchema


class RequestDemoQuery(BaseSchema):
    llm: Optional[str | None] = None
    question: str


class ResponseDemoQuery(BaseSchema):
    data: any


class DemoStructuredUserInfo(BaseSchema):
    name: str
    age: int
    profession: str
