from io import BytesIO

from minio import Minio

from app import settings
from app.core.config import MinIO
from app.core.libs.storage.storage_abc import StorageABC, ObjectResult

from typing import Generator, Any


class MinioStorage(StorageABC):
    """Minio storage implementation of the abstract base class."""

    def __init__(self, config: MinIO):

        self.minio_client = Minio(
            endpoint=config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.use_ssl,
            region=config.region,
        )

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

        if bucket_name is None:
            bucket_name = self.config['bucket']

        if length <= 0:
            length = len(data)

        # print(bucket_name, object_name, data, length)
        info = self.minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(data),
            length=length
        )
        # print(info)
        return ObjectResult(
            bucket_name=info.bucket_name,
            object_name=info.location,
            location=info.location,
        )

    def load_once(self, filename: str) -> bytes:
        response = self.minio_client.get_object(Bucket=self.config['bucket'], Key=filename)
        return response['Body'].read()

    def load_stream(self, filename: str) -> Generator[bytes, None, None]:
        response = self.minio_client.get_object(Bucket=self.config['bucket'], Key=filename)
        for chunk in response['Body']:
            yield chunk

    def download(self, filename: str, target_filepath: str) -> None:
        self.minio_client.download_file(self.config['bucket'], filename, target_filepath)

    def exists(self, filename: str) -> bool:
        try:
            self.minio_client.head_object(Bucket=self.config['bucket'], Key=filename)
            return True
        except:
            return False

    async def check_bucket_exists(self, bucket: str) -> Exception | None:
        exist = self.minio_client.bucket_exists(bucket)
        if not exist:
            try:
                location = settings.storage.minio.region
                await self.minio_client.make_bucket(bucket, location)

                policy = """
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": "*",
                                "Action": ["s3:GetObject"],
                                "Resource": ["arn:aws:s3:::{}/*".format(bucket)]
                            }
                        ]
                    }
                    """.strip()
                self.minio_client.set_bucket_policy(bucket, policy)

            except Exception as e:
                return e

        return None

    def delete(self, filename: str) -> None:
        self.minio_client.delete_object(Bucket=self.config['bucket'], Key=filename)
