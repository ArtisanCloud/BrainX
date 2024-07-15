import os
from base64 import b64decode
from datetime import datetime
from urllib.parse import urljoin
from minio import Minio
from io import BytesIO
from typing import Tuple, List
from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.media_resource.model import MediaResource
from app.dao.media_resource.media_resource import MediaResourceDAO, FindManyMediaResourcesOption, get_media_type
from app.schemas.base import ResponsePagination


class MediaResourceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.media_resource_dao = MediaResourceDAO(self.db)
        self.oss_client = None
        self.local_storage_path = os.path.join("public", "static")
        self.local_storage_url = urljoin(
            f"{settings.server.host}:{settings.server.port}",
            settings.media_resource.local_storage.storage_path,
        )

        if settings.media_resource.oss.enable:
            minio_config = settings.media_resource.oss.minio
            self.oss_client = Minio(
                minio_config.endpoint,
                access_key=minio_config.access_key,
                secret_key=minio_config.secret_key,
                secure=minio_config.use_ssl,
                region=minio_config.region,
            )
        else:
            local_storage_path = settings.media_resource.local_storage.storage_path
            if local_storage_path != "":
                self.local_storage_path = os.path.join(self.local_storage_path, local_storage_path)

    async def find_all_media_resources(self) -> Tuple[List[MediaResource], Exception | None]:
        try:
            return await self.media_resource_dao.find_all_media_resources()
        except SQLAlchemyError as e:
            return [], e

    async def find_many_media_resources(
            self, opt: FindManyMediaResourcesOption
    ) -> Tuple[
        List[MediaResource] | None,
        ResponsePagination | None,
        SQLAlchemyError | None,
    ]:
        try:
            return await self.media_resource_dao.find_many_media_resources(opt)
        except SQLAlchemyError as e:
            return None, None, e

    async def create_media_resource(
            self, resource: MediaResource
    ) -> Tuple[MediaResource | None, Exception | None]:
        try:
            return await self.media_resource_dao.create_media_resource(resource)
        except SQLAlchemyError as e:
            return None, e

    async def create_media_resources(
            self, resources: List[MediaResource]
    ) -> Tuple[List[MediaResource] | None, Exception | None]:
        try:
            return await self.media_resource_dao.create_media_resources(resources)
        except SQLAlchemyError as e:
            return None, e

    async def make_media_resource(self, bucket: str, handle) -> Tuple[MediaResource | None, Exception | None]:
        if self.oss_client:
            return await self.make_oss_resource(bucket, handle)
        else:
            return self.make_local_resource(bucket, handle)

    def make_local_resource(self, bucket: str, handle) -> Tuple[MediaResource | None, Exception | None]:
        try:
            filename = handle.filename
            filesize = handle.size

            bucket_path = os.path.join(self.local_storage_path, bucket)
            if not os.path.exists(bucket_path):
                os.makedirs(bucket_path)

            upload_path = os.path.join(bucket_path, filename)
            with open(upload_path, "wb") as f:
                f.write(handle.file.read())

            content_type = handle.content_type
            url = f"{self.local_storage_url}/{upload_path}"

            return MediaResource(
                bucket_name=bucket,
                filename=filename,
                size=filesize,
                url=url,
                content_type=content_type,
                resource_type=get_media_type(content_type),
            ), None
        except Exception as e:
            return None, e

    @staticmethod
    def get_oss_resource_uri( bucket: str, key: str) -> str:
        endpoint = settings.media_resource.oss.minio.endpoint
        return urljoin(endpoint, f"{bucket}/{key}")

    async def make_oss_resource(self, bucket: str, file: UploadFile) -> Tuple[MediaResource | None, Exception | None]:
        err = await self.check_bucket_exists(bucket)
        if err:
            return None, err

        try:
            object_name = f"{file.filename}"
            binary_data = BytesIO(await file.read())
            content_type = file.content_type

            info = self.oss_client.put_object(
                bucket, object_name, binary_data, len(binary_data), content_type=content_type
            )

            url = self.get_oss_resource_uri(bucket, info.object_name)

            return MediaResource(
                bucket_name=bucket,
                filename=info.object_name,
                size=len(binary_data),
                url=url,
                content_type=content_type,
                resource_type=get_media_type(content_type),
            ), None
        except Exception as e:
            return None, e

    async def make_oss_resource_by_base64_string(
            self, bucket: str, base64_data: str
    ) -> Tuple[MediaResource | None, Exception | None]:
        try:
            data = b64decode(base64_data, validate=True)
            return self.make_oss_resource_by_base64_data(bucket, data)
        except Exception as e:
            return None, e

    def make_oss_resource_by_base64_data(
            self, bucket: str, data: bytes
    ) -> Tuple[MediaResource | None, Exception | None]:
        try:
            if not self.oss_client.bucket_exists(bucket):
                return None, Exception(f"Bucket '{bucket}' does not exist")

            object_name = f"object_{datetime.now().timestamp()}"
            content_type = "image/png"

            info = self.oss_client.put_object(bucket, object_name, BytesIO(data), len(data), content_type=content_type)

            url = f"{bucket}/{object_name}"
            return MediaResource(
                bucket_name=bucket,
                filename=info.object_name,
                size=len(data),
                url=url,
                content_type=content_type,
                resource_type=get_media_type(content_type),
            ), None
        except Exception as e:
            return None, e

    async def check_bucket_exists(self, bucket: str) -> Exception | None:
        exist = self.oss_client.bucket_exists(bucket)

        if not exist:
            try:
                location = settings.media_resource.oss.minio.region
                await self.oss_client.make_bucket(bucket, location)

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
                self.oss_client.set_bucket_policy(bucket, policy)

            except Exception as e:
                return e

        return None
