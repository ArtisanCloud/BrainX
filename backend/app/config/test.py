from pydantic import BaseModel


class Test(BaseModel):
    db_url: str
