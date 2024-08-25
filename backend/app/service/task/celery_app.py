from celery import Celery

from app import settings
from app.config.celery import CeleryConfig


class CelerySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = create_celery_app()
        return cls._instance


def get_celery_app():
    return CelerySingleton()


def create_celery_app():
    app = Celery(
        'app',
        broker=settings.task.celery_broker_url,
        backend=settings.task.celery_result_backend
    )

    app.conf.update(
        imports=[
            'app.service.task.task',
            'app.service.task.rag.task'
        ],  # 确保任务模块被导入
        result_expires=settings.task.result_expires,  # 结果过期时间
        broker_connection_retry_on_startup=settings.task.broker_connection_retry_on_startup,  # 启动时重试
        # task_time_limit=settings.task.task_time_limit,  # 任务时间限制
        # task_soft_time_limit=settings.task.task_soft_time_limit,  # 软时间限制
        worker_concurrency=settings.task.worker_concurrency,  # 并发 worker 数量
        # worker_prefetch_multiplier=settings.task.worker_prefetch_multiplier,  # 每个 worker 同时处理的任务数量
        task_acks_on_failure_or_timeout=settings.task.task_acks_on_failure_or_timeout,  # 失败或超时任务是否确认
    )

    if settings.task.broker_use_ssl:
        app.conf.update(
            broker_use_ssl={
                "ssl_cert_reqs":  settings.task.ssl_cert_reqs,
                "ssl_ca_certs":  settings.task.ssl_ca_certs,
                "ssl_certfile": settings.task.ssl_cert_file,
                "ssl_keyfile":  settings.task.ssl_keyfile,
            }
        )

    return app


# Create and export a Celery instance
celery_app = create_celery_app()
