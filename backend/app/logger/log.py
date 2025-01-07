import logging
import os
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
import queue
import sys
import time
from app.config.config import settings


LOGS_DIRECTORY = os.path.join(".", "logs")
LOGS_TASK_DIRECTORY = os.path.join(LOGS_DIRECTORY, "task")
LOGS_TASK_RAG_DIRECTORY = os.path.join(LOGS_TASK_DIRECTORY, "rag")


class CustomExtraLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_context = kwargs.pop("extra", self.extra["extra"])
        # 设置App的名称到日志中
        if my_context is None:
            my_context = {"app": settings.server.project_name}
        # print(__name__)
        ############################################################
        # "[ %s ] %s" % (my_context, msg)：这是格式化字符串的方法，
        # 将 my_context 和 msg 插入到字符串中。
        # 最终的结果会是类似于 [context_value] message 的格式。
        ############################################################
        return "[%s] %s" % (my_context, msg), kwargs


def ensure_log_dir(log_dir: str, permissions: int = 0o755):
    """确保日志目录存在，并设置权限"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    # 设置目录权限
    os.chmod(log_dir, permissions)

    # 确保目录可写，否则抛出异常
    if not os.access(log_dir, os.W_OK):
        raise PermissionError(f"No write permission for directory: {log_dir}")


def get_logger(
    name,
    log_dir: str = LOGS_DIRECTORY,
    job: str = "web_api",
    level=logging.DEBUG,
) -> logging.Logger:
    # print("-------------------log name:",name)
    """logging to logfile as well as on console with thread-safety"""
    FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    # 创建日志目录
    ensure_log_dir(log_dir, permissions=0o755)

    # 创建 logger 实例
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)

    # 创建file logger handler
    if settings.log.file:
        # ------ info handler ------
        # 创建 info 级别的日志记录器
        info_handler = TimedRotatingFileHandler(
            filename=f"{log_dir}info.log",
            # 每天午夜进行轮转
            when="midnight",
            # 间隔1天（与 "midnight" 配合使用时，interval 设为 1）
            interval=settings.log.interval,
            # 保留最近n天的日志文件
            backupCount=settings.log.keep_days,
        )
        info_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        info_handler.setLevel(logging.INFO)

        # # 添加 info_handler 到 logger
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno <= logging.INFO
        info_handler.addFilter(info_filter)

        logger_instance.addHandler(info_handler)

        # ------ error handler ------

        # 创建 error 级别的日志记录器
        error_handler = TimedRotatingFileHandler(
            filename=f"{log_dir}error.log",
            when="midnight",
            interval=1,
            backupCount=settings.log.keep_days,
        )
        error_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        error_handler.setLevel(logging.ERROR)

        # 添加 error_handler 到 logger
        error_filter = logging.Filter()
        error_filter.filter = lambda record: record.levelno >= logging.ERROR
        error_handler.addFilter(error_filter)

        logger_instance.addHandler(error_handler)

    # Console logger handler 设置控制台输出
    if settings.log.console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        logger_instance.addHandler(console_handler)

    # 使用 QueueHandler 将日志消息放入队列
    # 创建队列
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger_instance.addHandler(queue_handler)

    # 创建并启动 QueueListener 在主线程中处理日志消息
    listener = QueueListener(
        log_queue,
    )
    # 启动 QueueListener
    listener.start()

    if settings.log.extra.elasticsearch.enable:
        import elasticsearch
        from app.logger.elastic_search_handler import ElasticSearchHandler

        # 初始化 Elasticsearch 客户端
        es_client = elasticsearch.Elasticsearch(
            hosts=settings.log.extra.elasticsearch.hosts,
            http_auth=(
                settings.log.extra.elasticsearch.username,
                settings.log.extra.elasticsearch.password,
            ),  # 使用你的用户名和密码
        )

        # 添加 ElasticsearchHandler
        es_handler = ElasticSearchHandler(es_client)
        es_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        logger_instance.addHandler(es_handler)
        logger_instance.info("Elasticsearch logging enabled")

    # 添加 Loki Log
    if settings.log.extra.loki.enable:
        from app.logger.loki_handler import LokiHandler
        loki_url = settings.log.extra.loki.url  # 从配置中获取 Loki 地址
        loki_labels = {
            "file_name":log_dir,
            "job": job,
            "level": settings.log.level,
            "service_name": name,
        }  # 从配置中获取 Loki 标签
        loki_handler = LokiHandler(url=loki_url, labels=loki_labels)
        loki_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        loki_handler.setLevel(level)
        logger_instance.addHandler(loki_handler)
        logger_instance.info("Loki logging enabled")

    logger_instance = CustomExtraLogAdapter(logger_instance, {"extra": None})
    return logger_instance


# 清理旧的日志文件
def clean_old_logs(log_dir: str, keep_days: int):
    """Recursively delete logs older than the specified retention period."""
    if not os.path.exists(log_dir):
        print(f"Log directory {log_dir} does not exist.")
        return

    now = time.time()
    for root, dirs, files in os.walk(log_dir):
        for filename in files:
            if filename.endswith(".log"):
                file_path = os.path.join(root, filename)
                try:
                    file_creation_time = os.path.getctime(file_path)
                    file_age_days = (now - file_creation_time) / (24 * 3600)
                    if file_age_days > keep_days:
                        os.remove(file_path)
                        print(f"Deleted old log file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")