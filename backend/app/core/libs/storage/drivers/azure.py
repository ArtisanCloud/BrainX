from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError
from io import BytesIO


class AzureStorage:
    def __init__(self, config:dict):
        self.account_name = config.get('ACCOUNT_NAME')
        self.account_key = config.get('ACCOUNT_KEY')
        self.container_name = config.get('CONTAINER_NAME')
        self.blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net",
                                                     credential=self.account_key)

    def save(self, filename, data):
        # 上传文件
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            print(f"Failed to upload file {filename} to Azure Blob Storage: {e}")
            raise

    def load_once(self, filename):
        # 下载文件（一次性加载）
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            data = blob_client.download_blob().readall()
            return data
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File {filename} not found in Azure Blob Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Azure Blob Storage: {e}")
            raise

    def load_stream(self, filename):
        # 下载文件（流式加载）
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            stream = blob_client.download_blob().content_as_bytes()
            return BytesIO(stream)
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File {filename} not found in Azure Blob Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Azure Blob Storage: {e}")
            raise

    def download(self, filename, target_filepath):
        # 下载文件到本地路径
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            with open(target_filepath, "wb") as f:
                blob_client.download_blob().download_to_stream(f)
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File {filename} not found in Azure Blob Storage")
        except Exception as e:
            print(f"Failed to download file {filename} from Azure Blob Storage to {target_filepath}: {e}")
            raise

    def exists(self, filename):
        # 检查文件是否存在
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False
        except Exception as e:
            print(f"Failed to check existence of file {filename} in Azure Blob Storage: {e}")
            raise

    def delete(self, filename):
        # 删除文件
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(filename)
            blob_client.delete_blob()
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File {filename} not found in Azure Blob Storage")
        except Exception as e:
            print(f"Failed to delete file {filename} from Azure Blob Storage: {e}")
            raise
