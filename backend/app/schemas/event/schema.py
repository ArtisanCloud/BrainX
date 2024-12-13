from app.schemas.base import BaseSchema


class RequestPublishEvent(BaseSchema):
    event_name: str
    message: str


class ResponsePublishEvent(BaseSchema):
    success: bool
