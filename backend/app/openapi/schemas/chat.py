from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(...)
    content: str = Field(...)

class RequestOpenAIChat(BaseModel):
    conversation_uuid: str = Field(...)
    app_uuid: str = Field(...)
    images: List[str] = Field(...)
    model: str = Field(...)
    messages: List[ChatMessage] = Field(...)


class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int = 0
    accepted_prediction_tokens: int = 0
    rejected_prediction_tokens: int = 0

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    completion_tokens_details: Optional[CompletionTokensDetails] = None

class ChatResponseMessage(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    delta: ChatResponseMessage
    logprobs: Optional[None] = None
    finish_reason: Optional[str] = None

class ResponseOpenAIChat(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    system_fingerprint: Optional[str] = None
    choices: List[Choice]
    usage: Optional[Usage] = None  # Make usage optional