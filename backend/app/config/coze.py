from pydantic import BaseModel
class Coze(BaseModel):
    api_base: str = "https://api.coze.cn/v1"
    api_key: str
    request_timeout: int = 300
