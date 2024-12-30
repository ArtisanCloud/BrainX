from typing import Dict

from pydantic import BaseModel


class CeleryConfig(BaseModel):
    enable: bool = False
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    # ssl 配置
    ssl_cert_reqs: str = None
    ssl_ca_certs: str = None
    ssl_cert_file: str = None
    ssl_keyfile: str = None
    result_expires: int = 3600
    # broker 配置
    broker_use_ssl: bool = False
    broker_connection_retry_on_startup: bool = True
    broker_connection_timeout: int = 30
    broker_heartbeat: int = 30
    # Socket 配置
    socket_connect_timeout: int = 30
    socket_timeout: int = 30
    # worker 配置
    worker_concurrency: int = 4  # 并发 worker 数量
    worker_prefetch_multiplier: int = 1  # 限制 worker 预取任务数
    # 队列的配置
    queue: Dict = {
        "default": "",
        "rag_queue": "rag_queue",
        "task_queue": "task_queue",
    }
    task_acks_on_failure_or_timeout: bool = True
    task_time_limit: int = 3600  # 任务最大执行时间
    task_soft_time_limit: int = 3000  # 软时间限制
    task_acks_late: bool = True  # 任务完成后才确认
    task_reject_on_worker_lost: bool = True  # worker 丢失时重新入队
    task_default_rate_limit: str = "1/s"  # 限制任务执行速率
    task_default_retry_delay: int = 5  # 重试延迟
