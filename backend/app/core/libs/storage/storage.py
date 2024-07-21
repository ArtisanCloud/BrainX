from io import BytesIO
from typing import Any

from app.core.config import Storage as StorageConfig
from app.core.libs.storage.drivers.local_storage import LocalStorage
from app.core.libs.storage.drivers.aliyun import AliyunStorage
from app.core.libs.storage.drivers.azure import AzureStorage
from app.core.libs.storage.drivers.google import GoogleStorage
from app.core.libs.storage.drivers.minio import MinioStorage
from app.core.libs.storage.drivers.s3 import S3Storage
from app.core.libs.storage.storage_abc import StorageABC, ObjectResult


class Storage:
    def __init__(self, config: StorageConfig):
        self.config = config
        self.storage_driver: StorageABC | None = None  # 先将 storage_driver 初始化为 None

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
                driver_instance = MinioStorage(self.config.minio)
            case "aliyun":
                driver_instance = AliyunStorage(**self.config.aliyun.dict())
            case "azure":
                driver_instance = AzureStorage(**self.config.azure.dict())
            case "google":
                driver_instance = GoogleStorage(**self.config.google.dict())
            case "s3":
                driver_instance = S3Storage(**self.config.s3.dict())
            case _:
                driver_instance = LocalStorage(self.config.local_storage)

        # print(driver_instance)
        return driver_instance

    def save(self,
             bucket_name: str,
             object_name: str,
             data: bytes,
             length: int,
             content_type: str = "application/octet-stream",
             metadata: dict | None = None,
             # sse: Sse | None = None,
             # progress: ProgressType | None = None,
             part_size: int = 0,
             num_parallel_uploads: int = 3,
             # tags: Tags | None = None,
             # retention: Retention | None = None,
             legal_hold: bool = False
             ) -> ObjectResult:
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.save(bucket_name, object_name, data, length)
        except Exception as e:
            raise RuntimeError(f"Failed to save file '{object_name}': {str(e)}")

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

    async def check_bucket_exists(self, bucket: str) -> Exception | None:
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return await self.storage_driver.check_bucket_exists(bucket)
        except Exception as e:
            raise RuntimeError(f"Failed to check existence of file '{bucket}': {str(e)}")

    def delete(self, filename):
        if not self.storage_driver:
            raise RuntimeError("Storage driver is not initialized.")
        try:
            return self.storage_driver.delete(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to delete file '{filename}': {str(e)}")
