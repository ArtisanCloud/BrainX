from typing import Dict

from pydantic import BaseModel


class CeleryConfig(BaseModel):
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    queue: Dict = {
        "default": "",
        "rag_queue": "rag_queue",
    }
    broker_use_ssl: bool = False
    ssl_cert_reqs: str = None
    ssl_ca_certs: str = None
    ssl_cert_file: str = None
    ssl_keyfile: str = None
    result_expires: int = 3600
    broker_connection_retry_on_startup: bool = True
    task_time_limit: int = 3600  # 任务最大执行时间
    task_soft_time_limit: int = 3000  # 软时间限制
    worker_concurrency: int = 4  # 并发 worker 数量
    worker_prefetch_multiplier: int = 1  # 每个 worker 同时处理的任务数量
    task_acks_on_failure_or_timeout: bool = True
