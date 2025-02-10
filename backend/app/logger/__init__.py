import logging
import psutil
from app.config.config import settings
from app.logger.log import get_logger

# 获取当前进程
current_process = psutil.Process()
job = "web_api"

logger = get_logger(__name__, job=job)

# Override Uvicorn logger
if hasattr(logger, 'logger'):
    base_logger = logger.logger
else:
    base_logger = logger

# 需要将Uvicorn的日志处理器和级别设置为与基础日志器相同
if settings.log.extra.loki.enable:
    logger = logging.getLogger("uvicorn")
    for handler in base_logger.handlers:
        logger.addHandler(handler)
    # 确保日志级别一致
    logger.setLevel(base_logger.level)

    # 这样做同样对 "uvicorn.error" 和 "uvicorn.access" 进行相同处理
    logging.getLogger("uvicorn.error").setLevel(base_logger.level)
    logging.getLogger("uvicorn.access").setLevel(base_logger.level)

    # logging.getLogger("uvicorn").handlers = base_logger.handlers
    # logging.getLogger("uvicorn.error").handlers = base_logger.handlers
    # logging.getLogger("uvicorn.access").handlers = base_logger.handlers
    #
    # # 确保日志级别一致
    # logging.getLogger("uvicorn").setLevel(base_logger.level)
    # logging.getLogger("uvicorn.error").setLevel(base_logger.level)
    # logging.getLogger("uvicorn.access").setLevel(base_logger.level)
