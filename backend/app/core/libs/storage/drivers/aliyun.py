
import oss2


class AliyunStorage:
    def __init__(self, config:dict):
        self.access_key_id = config.get('access_key')
        self.access_key_secret = config.get('secret_key')
        self.endpoint = config.get('endpoint')
        self.bucket_name = config.get('bucket_name')
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    def save(self, filename, data):
        # 上传文件
        self.bucket.put_object(filename, data)

    def load_once(self, filename):
        # 下载文件（一次性加载）
        obj = self.bucket.get_object(filename)
        return obj.read()

    def load_stream(self, filename):
        # 下载文件（流式加载）
        obj = self.bucket.get_object(filename)
        return obj.stream()

    def download(self, filename, target_filepath):
        # 下载文件到本地路径
        self.bucket.get_object_to_file(filename, target_filepath)

    def exists(self, filename):
        # 检查文件是否存在
        return self.bucket.object_exists(filename)

    def delete(self, filename):
        # 删除文件
        self.bucket.delete_object(filename)
