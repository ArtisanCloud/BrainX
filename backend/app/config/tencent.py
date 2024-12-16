from pydantic import BaseModel
class TencentHunYuan(BaseModel):
    api_base: str
    api_key: str
    request_timeout: int
