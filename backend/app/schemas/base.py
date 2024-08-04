from typing import Union, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from app.database.base import PER_PAGE
from app.utils.datetime import datetime_format


class Pagination(BaseModel):
    page: int | None
    page_size: int | None

    # def __init__(self, page: int = 1, page_size: int = PER_PAGE):
    #     self.page = page
    #     self.page_size = page_size


class ResponsePagination(BaseModel):
    limit: int
    page: int
    sort: bool
    total_rows: int
    total_pages: int

    # def __init__(self, limit: int, page: int, sort: bool, total_rows: int, total_pages: int):
    #     self.limit = limit
    #     self.page = page
    #     self.sort = sort
    #     self.total_rows = total_rows
    #     self.total_pages = total_pages


class ResponseSchema(BaseModel):
    """Generic response model for all responses"""
    api_id: str | None = None
    error: str | None = None
    message: str | None = None
    data: dict | list | None = None
    status_code: int | None = None

    # def __init__(self, api_id=None, error=None, message=None, data=None, status_code=None):
    #     super().__init__()
    #
    #     # self.api_id = api_id
    #     self.error = error
    #     self.message = message
    #     self.data = data
    #     self.status_code = status_code

    class Config:
        arbitrary_types_allowed = True


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class BaseObjectSchema(BaseSchema):
    id: Union[int, None] = None
    uuid: Union[UUID, None] = None
    created_at: Optional[str] = Field(None, description="Creation datetime")
    updated_at: Optional[str] = Field(None, description="Update datetime")

    @classmethod
    def from_orm(cls, obj):
        # 保存原始字段值
        original_fields = {
            'id': obj.id,
            'uuid': obj.uuid,
            'created_at': obj.created_at.strftime(datetime_format) if obj.created_at else None,
            'updated_at': obj.updated_at.strftime(datetime_format) if obj.updated_at else None
        }

        return original_fields
