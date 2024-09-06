from pydantic import BaseModel


class PowerX(BaseModel):
    access_key: str
    secret_key: str