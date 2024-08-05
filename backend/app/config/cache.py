from pydantic import BaseModel


class Redis(BaseModel):
    url: str


class Cache(BaseModel):
    redis: Redis
