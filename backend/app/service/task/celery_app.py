from celery import Celery

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
        broker=CeleryConfig.CELERY_BROKER_URL,
        backend=CeleryConfig.CELERY_RESULT_BACKEND
    )

    app.conf.update(
        result_expires=3600,
        result_backend=CeleryConfig.CELERY_RESULT_BACKEND,
        broker_connection_retry_on_startup=True,
        imports=['app.service.task.task'],  # 确保任务模块被导入
        worker_prefetch_multiplier=1,  # 每个 worker 同时处理的任务数量
        task_acks_on_failure_or_timeout=True,  # 失败或超时任务是否确认
    )

    if CeleryConfig.BROKER_USE_SSL:
        app.conf.update(
            broker_use_ssl={
                "ssl_cert_reqs": None,
                "ssl_ca_certs": None,
                "ssl_certfile": None,
                "ssl_keyfile": None,
            }
        )

    return app


# Create and export a Celery instance
celery_app = create_celery_app()


