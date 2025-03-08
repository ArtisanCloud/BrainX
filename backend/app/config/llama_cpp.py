from pydantic import BaseModel


class LlamaCPP(BaseModel):
    url: str
    timeout: int = 300

