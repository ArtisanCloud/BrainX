from pydantic import BaseModel


class Database(BaseModel):
    url: str
    table_name_vector_store: str
