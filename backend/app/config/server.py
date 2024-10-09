from enum import Enum
from typing import List

from pydantic import BaseModel

class ProjectType(str, Enum):
    Standalone = "standalone"
    Turbo = "turbo"


class Server(BaseModel):
    version: str
    project_name: str
    project_type: ProjectType = ProjectType.Standalone.value
    host: str
    port: int
    max_bytes: int
    cors_origins: List[str]
    worker_count: int
    environment: str
    server_render: bool
