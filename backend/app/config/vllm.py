from pydantic import BaseModel


class VLLM(BaseModel):
    url: str
    timeout: int = 300

