import logging
import os
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
import queue
import sys
import time
import elasticsearch
from app.config.config import settings
from app.logger.elastic_search_handler import ElasticSearchHandler


LOGS_DIRECTORY = "./logs/"
LOGS_TASK_DIRECTORY = "./logs/task/"
LOGS_TASK_RAG_DIRECTORY = LOGS_TASK_DIRECTORY+"rag"


class CustomExtraLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_context = kwargs.pop("extra", self.extra["extra"])
        return "[%s] %s" % (my_context, msg), kwargs


def get_logger(
    name, log_dir: str = LOGS_DIRECTORY, level=logging.DEBUG
) -> logging.Logger:
    # print("-------------------log name:",name)
    """logging to logfile as well as on console with thread-safety"""
    FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    elif not os.access(log_dir, os.W_OK):
        raise PermissionError(f"No write permission for directory: {log_dir}")

    # 创建队列
    log_queue = queue.Queue()

    # 创建 info 级别的日志记录器
    info_handler = TimedRotatingFileHandler(
        filename=log_dir + "info.log",
        # 每天午夜进行轮转
        when="midnight",
        # 间隔1天（与 "midnight" 配合使用时，interval 设为 1）
        interval=settings.log.interval,
        # 保留最近n天的日志文件
        backupCount=settings.log.keep_days,
    )
    info_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    info_handler.setLevel(logging.INFO)

    # 创建 error 级别的日志记录器
    error_handler = TimedRotatingFileHandler(
        filename=log_dir + "error.log",
        when="midnight",
        interval=1,
        backupCount=settings.log.keep_days,
    )
    error_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    error_handler.setLevel(logging.ERROR)

    # 创建 logger 实例
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)

    # # 添加 info_handler 到 logger
    info_filter = logging.Filter()
    info_filter.filter = lambda record: record.levelno <= logging.INFO
    info_handler.addFilter(info_filter)

    # # 添加 error_handler 到 logger
    error_filter = logging.Filter()
    error_filter.filter = lambda record: record.levelno >= logging.ERROR
    error_handler.addFilter(error_filter)

    # 设置控制台输出
    if settings.log.console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        logger_instance.addHandler(console_handler)

    ####### console 和 queue 二选一

    # 使用 QueueHandler 将日志消息放入队列
    queue_handler = QueueHandler(log_queue)
    logger_instance.addHandler(queue_handler)

    # 创建并启动 QueueListener 在主线程中处理日志消息
    listener = QueueListener(
        log_queue,
        info_handler,
        error_handler,
    )
    # 启动 QueueListener
    listener.start()

    if settings.log.extra["elasticsearch"].enable:
        # 初始化 Elasticsearch 客户端
        es_client = elasticsearch.Elasticsearch(
            hosts=settings.log.extra["elasticsearch"].hosts,
            http_auth=(
                settings.log.extra["elasticsearch"].username,
                settings.log.extra["elasticsearch"].password,
            ),  # 使用你的用户名和密码
        )

        # 添加 ElasticsearchHandler
        es_handler = ElasticSearchHandler(es_client)
        es_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
        logger_instance.addHandler(es_handler)
        logger_instance.info("Elasticsearch logging enabled")

    logger_instance = CustomExtraLogAdapter(logger_instance, {"extra": None})
    return logger_instance


# 清理旧的日志文件
def clean_old_logs(log_dir: str, keep_days: int):
    """删除指定目录下超过保留天数的日志文件"""
    if not os.path.exists(log_dir):
        print(f"Log directory {log_dir} does not exist.")
        return

    if not os.path.isdir(log_dir):
        print(f"The path {log_dir} is not a directory.")
        return
    
    now = time.time()  # 当前时间戳
    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".log"):
            try:
                file_creation_time = os.path.getctime(file_path)
                file_age_days = (now - file_creation_time) / (24 * 3600)  # 换算成天数
                if file_age_days > keep_days:
                    os.remove(file_path)
                    print(f"Deleted old log file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")