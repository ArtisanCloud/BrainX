from app import settings

# 由于monkey.patch_all() 会修改标准库行为
# Uvicorn 默认使用 asyncio 或 uvloop 事件循环
# 因此需要确保 Celery 使用的事件循环与 Uvicorn 的一致
# 只能单独为web api设置一个 celery_app单例，避免影响其他应用

class CelerySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = create_celery_app()
        return cls._instance


def get_celery_app():
    return CelerySingleton()


def create_celery_app():
    from celery import Celery

    app = Celery(
        'app',
        broker=settings.task.celery_broker_url,
        backend=settings.task.celery_result_backend
    )
    # print("create_celery_app broker url:", settings.task.celery_broker_url)
    # print("create_celery_app backend url:", settings.task.celery_result_backend)

    app.conf.update(
        imports=[
            'app.service.task.task',
            'app.service.task.rag.task',

            # custom tasks
            # 'app.openapi.service.custom.apqp.opl.service',

        ],  # 确保任务模块被导入
        
        # 设置任务的队列
        task_acks_on_failure_or_timeout=settings.task.task_acks_on_failure_or_timeout,  # 失败或超时任务是否确认
        task_time_limit=settings.task.task_time_limit,  # 任务时间限制
        task_acks_late=settings.task.task_acks_late,  # 任务完成后才确认
        task_soft_time_limit=settings.task.task_soft_time_limit,  # 软时间限制
        task_reject_on_worker_lost=settings.task.task_reject_on_worker_lost,  # worker 丢失时重新入队
        task_default_rate_limit=settings.task.task_default_rate_limit,  # 限制任务执行速率
        task_default_retry_delay=settings.task.task_default_retry_delay,  # 重试延迟

        # 设置 worker 配置
        worker_concurrency=settings.task.worker_concurrency,  # 并发 worker 数量
        worker_prefetch_multiplier=settings.task.worker_prefetch_multiplier,  # 每个 worker 同时处理的任务数量
        
        # 设置 Broker 配置
        broker_connection_retry_on_startup=settings.task.broker_connection_retry_on_startup,  # 启动时重试
        broker_connection_timeout=settings.task.broker_connection_timeout,  # 设置连接超时 (秒)
        broker_heartbeat=settings.task.broker_heartbeat,  # 设置心跳间隔 (秒)

        # 设置结果后端
        result_expires=settings.task.result_expires,  # 结果过期时间
        result_backend_transport_options={
            'socket_connect_timeout': settings.task.socket_connect_timeout,  # 连接 Redis 时的超时时间 (秒)
            'socket_timeout': settings.task.socket_timeout,          # 数据传输超时 (秒)
        },
    )

    if settings.task.broker_use_ssl:
        app.conf.update(
            broker_use_ssl={
                "ssl_cert_reqs": settings.task.ssl_cert_reqs,
                "ssl_ca_certs": settings.task.ssl_ca_certs,
                "ssl_certfile": settings.task.ssl_cert_file,
                "ssl_keyfile": settings.task.ssl_keyfile,
            }
        )

    return app


celery_app = None
if celery_app is None:
    celery_app = create_celery_app()

