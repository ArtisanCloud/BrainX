import os

from app.config.config import settings
from app.core.libs.storage.storage import Storage
from app.logger import logger
from app.utils.media import add_custom_mimetypes

# 全局变量，用于存储 Storage 实例
client_storage: Storage | None = None
default_local_storage_path = './storage/public/static/'


def load_app_tools():
    global client_storage
    client_storage = Storage(settings.storage)

    if not os.path.exists(default_local_storage_path):
        os.makedirs(default_local_storage_path)


# 在应用初始化时加载 app tools
load_app_tools()

# add custom mimetypes
add_custom_mimetypes()


def disable_gpu():
    import torch

    os.environ["MPS_VISIBLE_DEVICES"] = ""  # 禁用 GPU
    os.environ["USE_CPU"] = "1"

    torch.set_num_threads(8)  # 限制 CPU 线程
    device = torch.device("cpu")  # 强制使用 CPU
    logger.info(f"pytorch cuda is_available: {torch.cuda.is_available()}")  # 确保返回 False
    logger.info(f"pytorch mps is_available: {torch.mps.is_available()}")  # 确保返回 False

    # import tensorflow as tf
    # tf.config.set_visible_devices([], 'GPU')


if settings.agent.disable_gpu:
    disable_gpu()
