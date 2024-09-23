from app.schemas.base import BaseSchema


class RequestHelloWorld(BaseSchema):
    name: str
    message: str


class ResponseHelloWorld(BaseSchema):
    message: str
