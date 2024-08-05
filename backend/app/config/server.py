from typing import List

from pydantic import BaseModel


class Server(BaseModel):
    version: str
    project_name: str
    host: str
    port: int
    max_bytes: int
    cors_origins: List[str]
    worker_count: int
    environment: str
    server_render: bool
