from pydantic import BaseModel


class OpenAPI(BaseModel):
    access_key: str
    secret_key: str

