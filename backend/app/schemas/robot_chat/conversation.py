import uuid
from typing import Optional
from pydantic import constr

from app.models.robot_chat.conversation import Conversation, Message
from app.schemas.base import BaseSchema, Pagination, ResponsePagination, BaseObjectSchema


class MessageSchema(BaseObjectSchema):
    reply_to_message_uuid: Optional[str] = None
    content: str | None
    role: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: Message):
        # print(obj)
        base = super().from_orm(obj)
        return cls(
            **base,
            conversation_uuid=str(obj.conversation_uuid) if obj.conversation_uuid else None,  # 将 UUID 对象转换为字符串
            reply_to_message_uuid=str(obj.reply_to_message_uuid) if obj.reply_to_message_uuid else None,  # 处理 app_uuid 可能为 None 的情况
            content=obj.content,
            role=obj.role if obj.role else None ,
            type=obj.type,
        )

class ConversationSchema(BaseObjectSchema):
    user_uuid: Optional[str] = None
    app_uuid: Optional[str] = None
    app_model_config_uuid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None
    context: Optional[int] = None
    messages: Optional[list[MessageSchema]] = None

    @classmethod
    def from_orm(cls, obj: Conversation):
        # print(obj)
        base = super().from_orm(obj)
        return cls(
            **base,
            user_uuid=str(obj.user_uuid),  # 将 UUID 对象转换为字符串
            app_uuid=str(obj.app_uuid) if obj.app_uuid else None,  # 处理 app_uuid 可能为 None 的情况
            app_model_config_uuid=str(obj.app_model_config_uuid) if obj.app_model_config_uuid else None,
            name=obj.name,
            status=obj.status,
            context=obj.context,
        )


class RequestGetConversationList(BaseSchema):
    app_uuid: str
    pagination: Optional[Pagination] = None


class ResponseGetConversationList(BaseSchema):
    data: list[ConversationSchema]
    pagination: ResponsePagination


class RequestCreateConversation(ConversationSchema):
    name: constr(min_length=0, max_length=255)  # 允许为空
    app_uuid: constr(min_length=0, max_length=48)  # 允许为空


class ResponseCreateConversation(BaseSchema):
    conversation: ConversationSchema


class RequestPatchConversation(ConversationSchema):
    pass


class ResponsePatchConversation(BaseSchema):
    conversation: ConversationSchema


class ResponseDeleteConversation(BaseSchema):
    result: bool


def make_conversation(conversation: ConversationSchema) -> Conversation:
    return Conversation(
        uuid=uuid.uuid4(),  # 生成一个新的 UUID
        user_uuid=uuid.UUID(conversation.user_uuid) if conversation.user_uuid else None,
        app_uuid=uuid.UUID(conversation.app_uuid) if conversation.app_uuid else None,
        app_model_config_uuid=uuid.UUID(
            conversation.app_model_config_uuid) if conversation.app_model_config_uuid else None,
        name=conversation.name,
        status=conversation.status,
        context=conversation.context,
    )


class RequestGetMessageList(BaseSchema):
    conversation_uuid: str
    pagination: Optional[Pagination] = None


class ResponseGetMessageList(BaseSchema):
    data: list[MessageSchema]
    pagination: ResponsePagination
