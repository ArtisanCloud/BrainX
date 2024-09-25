from app.schemas.base import BaseSchema


class RequestHelloWorld(BaseSchema):
    name: str
    message: str


class ResponseHelloWorld(BaseSchema):
    message: str


class RequestEchoLongTime(BaseSchema):
    timeout: int


class ResponseEchoLongTime(BaseSchema):
    message: str
