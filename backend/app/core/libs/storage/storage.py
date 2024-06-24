from app.core.config import Storage as StorageConfig
from app.core.libs.storage.drivers.local_storage import LocalStorage
from app.core.libs.storage.drivers.aliyun import AliyunStorage
from app.core.libs.storage.drivers.azure import AzureStorage
from app.core.libs.storage.drivers.google import GoogleStorage
from app.core.libs.storage.drivers.s3 import S3Storage


class Storage:
    def __init__(self, config: StorageConfig):
        self.config = config
        self.storage_driver = None  # 先将 storage_driver 初始化为 None

        self._initialize_driver()

    def _initialize_driver(self):
        try:
            self.storage_driver = self._get_driver_instance()
        except ValueError as e:
            raise RuntimeError(f"Failed to initialize storage driver: {str(e)}")

    def _get_driver_instance(self):
        driver = self.config.driver
        driver_instance = None
        match driver:
            case "minio":
                driver_instance = S3Storage(**self.config.minio.dict())
            case "aliyun":
                driver_instance = AliyunStorage(**self.config.aliyun.dict())
            case "azure":
                driver_instance = AzureStorage(**self.config.azure.dict())
            case "google":
                driver_instance = GoogleStorage(**self.config.google.dict())
            case "s3":
                driver_instance = S3Storage(**self.config.s3.dict())
            case None:
                driver_instance = LocalStorage(self.config.local_storage)

        return driver_instance

    def save(self, filename, data):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.save(filename, data)
        except Exception as e:
            raise RuntimeError(f"Failed to save file '{filename}': {str(e)}")

    def load_once(self, filename):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.load_once(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to load file '{filename}': {str(e)}")

    def load_stream(self, filename):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.load_stream(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to load stream for file '{filename}': {str(e)}")

    def download(self, filename, target_filepath):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.download(filename, target_filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to download file '{filename}' to '{target_filepath}': {str(e)}")

    def exists(self, filename):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.exists(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to check existence of file '{filename}': {str(e)}")

    def delete(self, filename):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.delete(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to delete file '{filename}': {str(e)}")
