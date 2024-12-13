from typing import Dict, List

from pydantic import BaseModel


class Queue(BaseModel):
    name: str
    event_name: str


class Event(BaseModel):
    enable: bool = False
    driver: str = "rabbitMQ"

    host: str = None
    port: int = None
    user: str = "guest"
    password: str = "guest"
    default_event_queue: str = "queue_brainx"

    queues: List[Queue] = []
