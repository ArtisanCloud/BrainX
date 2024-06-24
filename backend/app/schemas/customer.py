from typing import List

from app.schemas.base import BaseSchema


class User(BaseSchema):
    id: str
    name: str


class ResponseUserList(BaseSchema):
    customers: List[User]