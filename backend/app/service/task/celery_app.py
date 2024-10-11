from celery import Celery
from app import settings
import click


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


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,  # 允许传递任意额外的参数
))
@click.option('--loglevel', default='info', help='Logging level.')
@click.option('-A', '--app', default=None, help='Celery app path.')
@click.option('-Q', '--queue', default=None, help='Queue to listen to.')
@click.option('-P', '--pool', default=None, help='Pool execution method (e.g., prefork, gevent).')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)  # 允许额外的命令行参数
def main(loglevel, app, queue, pool, args):
    """Start the Celery worker."""

    # 全局参数
    command = []

    # 如果有指定 app 则将 -A 选项添加到全局位置
    if app:
        command += ['-A', app]

    # 如果没有显式提供 worker 子命令，则手动添加
    if 'worker' not in args:
        command += ['worker']

    # 添加 loglevel
    command += ['--loglevel=' + loglevel]

    # 如果有指定 queue 则添加 -Q 选项
    if queue:
        command += ['-Q', queue]

    # 如果有指定 pool 则添加 -P 选项
    if pool:
        command += ['-P', pool]

    # 添加其余的命令行参数
    command += list(args)

    # 打印用于调试
    print("Executing Celery command: ", command)

    # 启动 celery worker
    celery_app.start(command)

if __name__ == "__main__":
    main()
