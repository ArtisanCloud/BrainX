from typing import List

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseORM, table_name_app, table_name_user, table_name_app_model_config, \
    table_name_conversation
from sqlalchemy import String, SmallInteger, BigInteger, Text, ForeignKey, UUID


class Conversation(BaseORM):
    __tablename__ = table_name_conversation

    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'))
    app_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_app + '.uuid'))
    app_model_config_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_app_model_config + '.uuid'))
    name = mapped_column(String)
    status = mapped_column(SmallInteger)
    context = mapped_column(Text)

    # app: Mapped["App"] = relationship(backref="conversation")

    # tenant: Mapped["User"] = relationship(backref="conversation")
    messages: Mapped[List["Message"]] = relationship(back_populates="conversation",
                                                     foreign_keys="[Message.conversation_uuid]")

    def __repr__(self):
        return (
            f"<Conversation(id={self.id}, "
            f"uuid={self.uuid}, "
            f"user_uuid={self.user_uuid}, "
            f"app_uuid={self.app_uuid}, "
            f"app_model_config_uuid={self.app_model_config_uuid}, "
            f"name={self.name}, "
            f"status={self.status}, "
            f"context={self.context})>"
        )

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'user_uuid': self.user_uuid,
            'app_uuid': self.app_uuid,
            'app_model_config_uuid': self.app_model_config_uuid,
            'name': self.name,
            'status': self.status,
            'context': self.context
        }

table_name_message = 'message'


class Message(BaseORM):
    __tablename__ = table_name_message

    conversation_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_conversation + '.uuid'))
    reply_to_message_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_message + '.uuid'))
    content = mapped_column(String)
    role = mapped_column(SmallInteger)
    type = mapped_column(SmallInteger)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages", foreign_keys=[conversation_uuid])
    replies: Mapped[List["Message"]] = relationship(back_populates="question", foreign_keys=[reply_to_message_uuid])
    question: Mapped["Message"] = relationship(back_populates="replies", foreign_keys=[reply_to_message_uuid],
                                               remote_side="Message.uuid")

    # def __init__(self, conversation_id, content, role, type=None):
    #     super().__init__()
    #     self.conversation_id = conversation_id
    #     self.content = content
    #     self.role = role
    #     self.type = type
