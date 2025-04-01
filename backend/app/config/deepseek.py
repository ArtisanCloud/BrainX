from pydantic import BaseModel
class DeepSeek(BaseModel):
    api_base: str
    api_key: str
    request_timeout: int
