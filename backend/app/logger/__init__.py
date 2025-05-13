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


# print("base_logger: ", base_logger)

def setup_uvicorn_logging():
    print("🚀 开始配置 Uvicorn 日志")

    # 🚀 处理 "uvicorn" 服务器日志
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    for handler in base_logger.handlers:
        uvicorn_logger.addHandler(handler)
    uvicorn_logger.setLevel(base_logger.level)

    # 🚀 处理 "uvicorn.access" 访问日志
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers.clear()  # 🚨 清空默认 stdout
    for handler in base_logger.handlers:
        uvicorn_access_logger.addHandler(handler)  # ✅ 添加 LokiHandler
    uvicorn_access_logger.setLevel(base_logger.level)

    # 🚀 处理 "uvicorn.error" 服务器错误日志
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers.clear()
    for handler in base_logger.handlers:
        uvicorn_error_logger.addHandler(handler)
    uvicorn_error_logger.setLevel(base_logger.level)

    print("🚀 Uvicorn 日志已绑定 Loki")
    # print("uvicorn_access_logger handlers: ", uvicorn_access_logger.handlers)

