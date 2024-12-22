from typing import Optional, Dict

from pydantic import BaseModel


class JobStoreConfig(BaseModel):
    type: str
    url: Optional[str]
    host: Optional[str]
    port: Optional[int]
    db: Optional[int]
    username: Optional[str]
    password: Optional[str]


class ExecutorsConfig(BaseModel):
    type: str
    max_workers: int


class JobDefaultsConfig(BaseModel):
    coalesce: bool
    max_instances: int


class Schedule(BaseModel):
    driver: str
    enable: bool = False
    job_stores: Dict[str, JobStoreConfig]
    executors: Dict[str, ExecutorsConfig]
    job_defaults: JobDefaultsConfig
