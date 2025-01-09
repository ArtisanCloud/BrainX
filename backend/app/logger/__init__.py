import psutil
from app.logger.log import get_logger

# 获取当前进程
current_process = psutil.Process()
job = "web_api"

logger = get_logger(__name__, job=job)

# logger.info('Logger initiated')
