from typing import Optional, Dict

from pydantic import BaseModel, AnyUrl


class JobStoreConfig(BaseModel):
    type: str
    url: Optional[AnyUrl]  # Use `AnyUrl` to validate the URL format


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
