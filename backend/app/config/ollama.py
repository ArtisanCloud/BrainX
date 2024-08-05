from pydantic import BaseModel


class OLLAMA(BaseModel):
    url: str

