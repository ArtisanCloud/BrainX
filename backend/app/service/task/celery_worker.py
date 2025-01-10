from gevent import monkey

monkey.patch_all()
# monkey.patch_all(ssl=False, aiohttp=False)

from billiard import util

# 增加缓冲区大小
util._process_buffer_size = 1024

# 如果上面的方法不行，可以尝试调整 multiprocessing 的缓冲区
import multiprocessing

multiprocessing.get_start_method()  # 获取当前启动方法，确保是合适的

import click
from celery import Celery


from app import settings


def create_celery_worker():
    app = Celery(
        "app",
        broker=settings.task.celery_broker_url,
        backend=settings.task.celery_result_backend,
    )
    

    app.conf.update(
        imports=[
            "app.service.task.task",
            "app.service.task.rag.task",
            # custom tasks
            # 'app.openapi.service.custom.apqp.opl.service',
        ],  # 确保任务模块被导入
        worker_stdout=None,  # 禁止 Celery 在终端输出日志
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
            "socket_connect_timeout": settings.task.socket_connect_timeout,  # 连接 Redis 时的超时时间 (秒)
            "socket_timeout": settings.task.socket_timeout,  # 数据传输超时 (秒)
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


celery_worker = create_celery_worker()

# 是否禁用 Celery 默认的日志输出
if not settings.log.console:
    from celery import signals
    @signals.setup_logging.connect
    def disable_celery_logging(**kwargs):
        import logging
        for logger_name in ['celery', 'celery.worker', 'celery.task']:
            logger = logging.getLogger(logger_name)
            logger.handlers = []  # 移除默认处理器
            logger.propagate = False  # 禁用日志向上传播

# 设置启动参数
@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option("--loglevel", default="info", help="Logging level.")
@click.option("-A", "--app", default=None, help="Celery app path.")
@click.option("-Q", "--queue", default=None, help="Queue to listen to.")
@click.option(
    "-P", "--pool", default=None, help="Pool execution method (e.g., prefork, gevent)."
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(loglevel, app, queue, pool, args):
    """Start the Celery worker."""

    command = []

    if app:
        command += ["-A", app]

    if "worker" not in args:
        command += ["worker"]

    command += ["--loglevel=" + loglevel]

    if queue:
        command += ["-Q", queue]

    if pool:
        command += ["-P", pool]

    command += list(args)

    print("Executing Celery command: ", command)

    celery_worker.start(command)


if __name__ == "__main__":
    main()
