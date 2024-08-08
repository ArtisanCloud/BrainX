from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.originaztion.user import User
from app.schemas.base import BaseObjectSchema


class UserRole(str, Enum):
    """Enum for tenant roles"""
    ADMIN = "admin"
    CUSTOMER = "tenant"


class UserStatus(str, Enum):
    """Enum for tenant system"""
    ACTIVE = "active"
    SUSPENDED = "suspended"


class UserTokenData(BaseModel):
    """User token data"""
    uuid: str
    role: UserRole
    email: EmailStr


class UserSchema(BaseObjectSchema):
    account: Optional[str]
    name: Optional[str]
    nick_name: Optional[str]
    desc: Optional[str]
    position_id: Optional[str]
    job_title: Optional[str]
    department_id: Optional[int]
    mobile_phone: Optional[str]
    gender: Optional[str]
    email: Optional[str]
    external_email: Optional[str]
    avatar: Optional[str]
    password: Optional[str]
    status: Optional[str]
    is_reserved: Optional[bool]
    is_activated: Optional[bool]
    we_work_user_id: Optional[str]

    @classmethod
    def from_orm(cls, obj: User):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            account=obj.account,
            name=obj.name,
            nick_name=obj.nick_name,
            desc=obj.desc,
            position_id=obj.position_id,
            job_title=obj.job_title,
            department_id=obj.department_id,
            mobile_phone=obj.mobile_phone,
            gender=obj.gender,
            email=obj.email,
            external_email=obj.external_email,
            avatar=obj.avatar,
            password=obj.password,
            status=obj.status,
            is_reserved=obj.is_reserved,
            is_activated=obj.is_activated,
            we_work_user_id=obj.we_work_user_id,
        )


class ResponseGetUser(UserSchema):
    """User models for response"""


class UserLoginModel(BaseModel):
    """User logincart models"""
    email: EmailStr
    password: str


class TokenType(str, Enum):
    bearer = "bearer"


class UserTokenResponseModel(BaseModel):
    """User token models"""
    user_uuid: UUID
    access_token: str
    token_type: TokenType = TokenType.bearer
    user_role: UserRole
    user_status: UserStatus
