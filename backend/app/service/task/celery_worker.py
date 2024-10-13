from gevent import monkey
import click
from celery import Celery

monkey.patch_all()

from app import settings


def create_celery_worker():
    app = Celery(
        'app',
        broker=settings.task.celery_broker_url,
        backend=settings.task.celery_result_backend
    )

    app.conf.update(
        imports=[
            'app.service.task.task',
            'app.service.task.rag.task',

            # custom tasks
            'app.openapi.service.custom.apqp.opl.service',

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


celery_worker = create_celery_worker()


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--loglevel', default='info', help='Logging level.')
@click.option('-A', '--app', default=None, help='Celery app path.')
@click.option('-Q', '--queue', default=None, help='Queue to listen to.')
@click.option('-P', '--pool', default=None, help='Pool execution method (e.g., prefork, gevent).')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def main(loglevel, app, queue, pool, args):
    """Start the Celery worker."""

    command = []

    if app:
        command += ['-A', app]

    if 'worker' not in args:
        command += ['worker']

    command += ['--loglevel=' + loglevel]

    if queue:
        command += ['-Q', queue]

    if pool:
        command += ['-P', pool]

    command += list(args)

    print("Executing Celery command: ", command)

    celery_worker.start(command)


if __name__ == "__main__":
    main()
