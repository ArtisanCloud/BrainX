import os

from app.config.config import settings
from app.core.libs.storage.drivers.local_storage import LocalStorage
from app.config.storage import LocalStorage as LocalStorageConfig
from app.core.libs.storage.storage import Storage
from app.logger import logger
from app.utils.media import add_custom_mimetypes

# 全局变量，用于存储 Storage 实例
oss_client_storage: Storage | None = None
local_client_storage: LocalStorage | None = None
default_local_storage_path = './storage'


def load_app_tools():
    global oss_client_storage
    oss_client_storage = Storage(settings.storage)

    if not os.path.exists(default_local_storage_path):
        os.makedirs(default_local_storage_path)

    global local_client_storage
    local_client_storage = LocalStorage(LocalStorageConfig(
        storage_path=default_local_storage_path,
    ))


# 在应用初始化时加载 app tools
load_app_tools()

# add custom mimetypes
add_custom_mimetypes()
