from google.cloud import storage
from google.cloud.exceptions import NotFound
from io import BytesIO


class GoogleStorage:
    def __init__(self, config:dict):
        self.bucket_name = config.get('BUCKET_NAME')
        self.client = storage.Client()

    def save(self, filename, data):
        # 上传文件
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_string(data)
        except Exception as e:
            print(f"Failed to upload file {filename} to Google Cloud Storage: {e}")
            raise

    def load_once(self, filename):
        # 下载文件（一次性加载）
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            data = blob.download_as_string()
            return data
        except NotFound:
            raise FileNotFoundError(f"File {filename} not found in Google Cloud Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Google Cloud Storage: {e}")
            raise

    def load_stream(self, filename):
        # 下载文件（流式加载）
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            stream = BytesIO()
            blob.download_to_file(stream)
            stream.seek(0)
            return stream
        except NotFound:
            raise FileNotFoundError(f"File {filename} not found in Google Cloud Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Google Cloud Storage: {e}")
            raise

    def download(self, filename, target_filepath):
        # 下载文件到本地路径
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            with open(target_filepath, "wb") as f:
                blob.download_to_file(f)
        except NotFound:
            raise FileNotFoundError(f"File {filename} not found in Google Cloud Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Google Cloud Storage to {target_filepath}: {e}")
            raise

    def exists(self, filename):
        # 检查文件是否存在
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.reload()
            return True
        except NotFound:
            return False
        except Exception as e:
            print(f"Failed to check existence of file {filename} in Google Cloud Storage: {e}")
            raise

    def delete(self, filename):
        # 删除文件
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.delete()
        except NotFound:
            raise FileNotFoundError(f"File {filename} not found in Google Cloud Storage")
        except Exception as e:
            print(f"Failed to delete file {filename} from Google Cloud Storage: {e}")
            raise
