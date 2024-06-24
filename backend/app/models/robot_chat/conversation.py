from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from sqlalchemy import Column, String, SmallInteger, BigInteger, Text, ForeignKey


table_name_conversation = 'conversation'


class Conversation(BaseModel):
    __tablename__ = table_name_conversation

    user_id = mapped_column('user_id', BigInteger, ForeignKey('customers.id'))
    app_id = mapped_column('app_id', BigInteger, ForeignKey('apps.id'))
    name = mapped_column('name', String)
    status = mapped_column('system', SmallInteger)
    context = mapped_column('context', Text)

    # app = relationship("App", backref="conversation")
    # customer = relationship("User", backref="conversation")

    def __init__(self, user_id, app_id, name, status=None, context=None):
        super().__init__()
        self.user_id = user_id
        self.app_id = app_id
        self.name = name
        self.status = status
        self.context = context


table_name_message = 'message'
class Message(BaseModel):
    __tablename__ = table_name_message

    conversation_id = mapped_column('conversation_id', BigInteger, ForeignKey('conversations.id'))
    content = mapped_column('content', String)
    role = mapped_column('role', SmallInteger)
    type = mapped_column('type', SmallInteger)

    # conversation = relationship(Conversation, backref="message")

    def __init__(self, conversation_id, content, role, type=None):
        super().__init__()
        self.conversation_id = conversation_id
        self.content = content
        self.role = role
        self.type = type
