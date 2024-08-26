from pydantic import BaseModel


class Database(BaseModel):
    async_url: str
    sync_url: str
    table_name_vector_store: str
    echo_log: bool = True
