from pydantic import BaseModel


class Redis(BaseModel):
    url: str


class Cache(BaseModel):
    driver: str = "redis"
    redis: Redis
