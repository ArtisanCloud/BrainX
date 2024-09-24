from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class DemoStructuredUserInfo(BaseModel):
    """用户的结构化信息类"""

    name: str = Field(
        default=None, description="用户的姓名"
    )
    age: int = Field(
        default=None, description="用户的年龄"
    )
    profession: str = Field(
        default=None, description="用户的职业"
    )


class ResponseDemoFormatQuery(BaseSchema):
    data: DemoStructuredUserInfo
