from pydantic import BaseModel
class OpenAI(BaseModel):
    llm_name: str
    api_base: str
    api_key: str
    request_timeout: int