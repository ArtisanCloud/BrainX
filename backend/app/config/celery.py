from pydantic import BaseModel


class CeleryConfig(BaseModel):
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    broker_use_ssl: bool = False
    ssl_cert_reqs: str = None
    ssl_ca_certs: str = None
    ssl_cert_file: str = None
    ssl_keyfile: str = None
    result_expires: int
    broker_connection_retry_on_startup: bool
