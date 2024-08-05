from pydantic import BaseModel
class BaiduQianfan(BaseModel):
    api_key: str
    secret_key: str
    request_timeout: int
