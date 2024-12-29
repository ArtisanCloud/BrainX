from pydantic import BaseModel


class Coze(BaseModel):
    api_base: str = "https://api.coze.cn/v1"
    api_key: str
    request_timeout: int = 300
    bot_id: str = ""  # 默认值为空字符串
    user_id: str = ""  # 默认值为空字符串
    conversation_id: str = ""  # 默认值为空字符串
