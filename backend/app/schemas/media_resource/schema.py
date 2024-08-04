from typing import List, Union, Optional

from pydantic import BaseModel

from app.models import MediaResource
from app.schemas.base import BaseSchema, Pagination, ResponsePagination, BaseObjectSchema


class MediaResourceSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    bucket_name: str
    filename: str
    size: int
    is_local_stored: bool
    url: str
    content_type: str
    resource_type: str
    sort_index: Union[int, None] = None

    @classmethod
    def from_orm(cls, obj: MediaResource):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            tenant_uuid=str(obj.tenant_uuid),
            created_user_by=str(obj.created_user_by),
            bucket_name=obj.bucket_name,
            filename=obj.filename,
            size=obj.size,
            is_local_stored=obj.is_local_stored,
            url=obj.url,
            content_type=obj.content_type,
            resource_type=obj.resource_type,
            sort_index=obj.sort_index,
        )


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
    sortIndex: int


class ResponseCreateMediaResource(BaseModel):
    media_resource: MediaResourceSchema
    is_oss: bool


class ResponseGetMediaResource(BaseSchema):
    data: MediaResourceSchema
