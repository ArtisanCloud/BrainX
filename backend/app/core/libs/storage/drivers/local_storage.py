import os
import shutil
from io import BytesIO
from typing import Any
from urllib.parse import urljoin

from app.core.config import LocalStorage, settings
from app.core.libs.storage.storage_abc import ObjectResult


class LocalStorage:
    def __init__(self, config: LocalStorage):
        base_path = config.storage_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        server_host = settings.server.host
        server_port = settings.server.port
        base_url = f"{server_host}:{server_port}"

        self.local_storage_path = os.path.join(base_path, "public", "static")
        self.local_storage_url = urljoin(f"http://{base_url}/", "static")
        # print(self.local_storage_path, self.local_storage_url)

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
             ) -> Any:

        bucket_path = os.path.join(self.local_storage_path, bucket_name)
        if not os.path.exists(bucket_path):
            os.makedirs(bucket_path)

        upload_path = os.path.join(bucket_path, object_name)
        with open(upload_path, "wb") as f:
            f.write(data)

        info = ObjectResult(
            bucket_name=bucket_name,
            object_name=object_name,
        )

        return info

    def load_once(self, filename):
        # 加载文件（一次性加载）
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'rb') as f:
            data = f.read()
        return data

    def load_stream(self, filename):
        # 加载文件（流式加载）
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'rb') as f:
            stream = BytesIO(f.read())
        return stream

    def download(self, filename, target_filepath):
        # 下载文件到本地路径
        file_path = os.path.join(self.base_path, filename)
        shutil.copyfile(file_path, target_filepath)

    def exists(self, filename):
        # 检查文件是否存在
        file_path = os.path.join(self.base_path, filename)
        return os.path.exists(file_path)

    async def check_bucket_exists(self, bucket: str) -> Exception | None:
        bucket_path = os.path.join(self.local_storage_path, bucket)
        # 检查路径是否存在
        if not os.path.exists(bucket_path):
            try:
                # 如果路径不存在，则创建它
                os.makedirs(bucket_path)
            except Exception as e:
                return e  # 如果创建路径失败，返回异常

        return None

    def delete(self, filename):
        # 删除文件
        file_path = os.path.join(self.base_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File {filename} not found in local storage")
