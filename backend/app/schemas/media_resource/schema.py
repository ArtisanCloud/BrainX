from typing import List, Union

from pydantic import BaseModel

from app.schemas.base import BaseSchema, Pagination, ResponsePagination, BaseObjectSchema


class MediaResourceSchema(BaseObjectSchema):
    user_id: Union[int, None] = None
    bucket_name: str
    filename: str
    size: int
    is_local_stored: bool
    url: str
    content_type: str
    resource_type: str
    sort_index: Union[int, None] = None


class RequestGetMediaResourceList(Pagination):
    like_name: str = None
    order_by: str = None


class ResponseGetMediaResourceList(BaseSchema):
    data: List[MediaResourceSchema]
    pagination: ResponsePagination


class RequestCreateMediaResourceByBase64(BaseModel):
    mediaName: str
    bucketName: str
    base64Data: str


class ResponseCreateMediaResource(BaseModel):
    media_resource: MediaResourceSchema
    is_oss: bool
