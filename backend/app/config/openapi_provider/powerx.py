from pydantic import BaseModel


class PowerX(BaseModel):
    base_url: str = "http://powerx.example.com/api/v1"
    access_key: str
    secret_key: str
