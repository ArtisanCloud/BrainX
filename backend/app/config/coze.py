from pydantic import BaseModel
class Coze(BaseModel):
    api_base: str
    api_key: str
    request_timeout: int = 300
