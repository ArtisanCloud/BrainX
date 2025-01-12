import logging
import psutil
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

logging.getLogger("uvicorn").handlers = base_logger.handlers
logging.getLogger("uvicorn.error").handlers = base_logger.handlers
logging.getLogger("uvicorn.access").handlers = base_logger.handlers

# 确保日志级别一致
logging.getLogger("uvicorn").setLevel(base_logger.level)
logging.getLogger("uvicorn.error").setLevel(base_logger.level)
logging.getLogger("uvicorn.access").setLevel(base_logger.level)
