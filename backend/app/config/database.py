from pydantic import BaseModel

class Database(BaseModel):
    dsn: str
    db_schema: str = "public"
    echo_log: bool = True
