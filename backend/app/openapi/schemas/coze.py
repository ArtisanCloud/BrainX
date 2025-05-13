
from typing import Dict, List, Optional
from cozepy import Message
from pydantic import BaseModel


class RequestChat(BaseModel):
    input: str
    bot_id: str
    user_id: str
    conversation_id: Optional[str] = None
    additional_messages: Optional[List[Message]] = None
    custom_variables: Optional[Dict[str, str]] = None
    auto_save_history: bool = True
    meta_data: Optional[Dict[str, str]] = None
    poll_timeout: Optional[int] = None


class ResponseChat(BaseModel):
    content:str


