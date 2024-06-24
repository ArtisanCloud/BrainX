import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

LOGS_DIRECTORY = './logs/'

if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)


class CustomExtraLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_context = kwargs.pop('extra', self.extra['extra'])
        return '[%s] %s' % (my_context, msg), kwargs


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    """"logging to logfile as well as on console"""
    FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    # 创建 info 级别的日志记录器
    info_handler = TimedRotatingFileHandler(filename=LOGS_DIRECTORY + 'info.log', when="midnight", interval=1,
                                            backupCount=7)
    info_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    info_handler.setLevel(logging.INFO)

    # 创建 error 级别的日志记录器
    error_handler = TimedRotatingFileHandler(filename=LOGS_DIRECTORY + 'error.log', when="midnight", interval=1,
                                             backupCount=7)
    error_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    error_handler.setLevel(logging.ERROR)

    # 创建 logger 实例
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)

    # 添加 info_handler 到 logger
    info_filter = logging.Filter()
    info_filter.filter = lambda record: record.levelno <= logging.INFO
    info_handler.addFilter(info_filter)
    logger_instance.addHandler(info_handler)

    # 添加 error_handler 到 logger
    error_filter = logging.Filter()
    error_filter.filter = lambda record: record.levelno >= logging.ERROR
    error_handler.addFilter(error_filter)
    logger_instance.addHandler(error_handler)

    # 设置控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(FORMAT, datefmt=TIME_FORMAT))
    logger_instance.addHandler(console_handler)

    logger_instance = CustomExtraLogAdapter(logger_instance, {"extra": None})
    return logger_instance


logger = get_logger(__name__)

# logger.info('Logger initiated')
