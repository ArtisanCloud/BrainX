import boto3
from botocore.config import Config

from app.core.libs.storage.storage_abc import StorageABC

from typing import Generator, Union


class S3Storage(StorageABC):
    """S3 storage implementation of the abstract base class."""

    def __init__(self, config: dict):
        super().__init__(config)
        # Initialize the S3 client
        self.s3_client = boto3.client(
            's3',
            aws_secret_access_key=config.get('S3_SECRET_KEY'),
            aws_access_key_id=config.get('S3_ACCESS_KEY'),
            endpoint_url=config.get('S3_ENDPOINT'),
            region_name=config.get('S3_REGION'),
            config=Config(s3={'addressing_style': config.get('S3_ADDRESS_STYLE')})
        )

    def save(self, filename: str, data: bytes) -> None:
        self.s3_client.put_object(Bucket=self.config['bucket'], Key=filename, Body=data)

    def load_once(self, filename: str) -> bytes:
        response = self.s3_client.get_object(Bucket=self.config['bucket'], Key=filename)
        return response['Body'].read()

    def load_stream(self, filename: str) -> Generator[bytes, None, None]:
        response = self.s3_client.get_object(Bucket=self.config['bucket'], Key=filename)
        for chunk in response['Body']:
            yield chunk

    def download(self, filename: str, target_filepath: str) -> None:
        self.s3_client.download_file(self.config['bucket'], filename, target_filepath)

    def exists(self, filename: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.config['bucket'], Key=filename)
            return True
        except:
            return False

    def delete(self, filename: str) -> None:
        self.s3_client.delete_object(Bucket=self.config['bucket'], Key=filename)
