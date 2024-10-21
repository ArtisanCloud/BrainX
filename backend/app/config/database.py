from pydantic import BaseModel

class Database(BaseModel):
    dsn: str
    db_schema: str = "public"
    table_name_vector_store: str
    echo_log: bool = True
