import os
from io import BytesIO

from app.core.config import LocalStorage


class LocalStorage:
    def __init__(self, config: LocalStorage):
        self.base_path = config.storage_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def save(self, filename, data):
        # 保存文件到本地路径
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'wb') as f:
            f.write(data)

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

    def delete(self, filename):
        # 删除文件
        file_path = os.path.join(self.base_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File {filename} not found in local storage")
