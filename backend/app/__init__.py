from app.core.config import settings
from app.core.libs.storage.storage import Storage

# 全局变量，用于存储 Storage 实例
lib_local_storage = None


def load_app_tools():
    global lib_local_storage
    local_setting = settings.storage
    local_setting.driver = None
    lib_local_storage = Storage(settings.storage)


# 在应用初始化时加载 app tools
load_app_tools()
