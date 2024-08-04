from base64 import b64decode
from datetime import datetime
from urllib.parse import urljoin
from typing import Tuple, List
from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import client_storage
from app.core.config import settings
from app.core.libs.storage.storage import Storage
from app.models import User
from app.models.media_resource.model import MediaResource
from app.dao.media_resource.media_resource import MediaResourceDAO, FindManyMediaResourcesOption, get_media_type
from app.schemas.base import ResponsePagination
from app.utils.media import remove_base64_prefix, get_content_type_from_base64, get_file_type_from_magic_numbers


class MediaResourceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.media_resource_dao = MediaResourceDAO(self.db)
        self.oss_client: Storage | None = None

        self.oss_client = client_storage

    async def find_all_media_resources(self) -> Tuple[List[MediaResource], SQLAlchemyError | None]:
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
    ) -> Tuple[MediaResource | None, SQLAlchemyError | None]:
        try:
            return await self.media_resource_dao.create_media_resource(resource)
        except SQLAlchemyError as e:
            return None, e

    async def create_media_resources(
            self, resources: List[MediaResource]
    ) -> Tuple[List[MediaResource] | None, SQLAlchemyError | None]:
        try:
            return await self.media_resource_dao.create_media_resources(resources)
        except SQLAlchemyError as e:
            return None, e

    async def make_media_resource(self, bucket: str, handle) -> Tuple[MediaResource | None, SQLAlchemyError | None]:
        return await self.make_oss_resource(bucket, handle)

    @staticmethod
    def get_oss_resource_uri(bucket: str, key: str) -> str:
        endpoint = settings.storage.minio.endpoint
        return urljoin(endpoint, f"{bucket}/{key}")

    async def make_oss_resource(self, bucket: str, file: UploadFile) -> Tuple[MediaResource | None, SQLAlchemyError | None]:
        err = await self.check_bucket_exists(bucket)
        if err:
            return None, err

        try:
            object_name = f"{file.filename}"
            binary_data = await file.read()
            content_type = file.content_type

            info = self.oss_client.save(
                bucket, object_name, binary_data, length=len(binary_data),
                content_type=content_type
            )

            url = self.get_oss_resource_uri(bucket, info.object_name)
            if info.location != '':
                url = info.location
            # print(info, url)

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
            self, user: User,
            bucket: str, base64_data: str,
            media_name: str = None, sort_index: int = None,
    ) -> Tuple[MediaResource | None, SQLAlchemyError | None]:

        content_type = self.determine_content_type(base64_data)
        if content_type is None:
            return None, Exception(f"Invalid base64 data content type")

        base64_data = remove_base64_prefix(base64_data)

        try:
            data = b64decode(base64_data, validate=True)
            return await self.make_oss_resource_by_base64_data(
                user, bucket,
                data, content_type,
                media_name, sort_index
            )
        except Exception as e:
            return None, e

    async def make_oss_resource_by_base64_data(
            self,
            user: User, bucket: str,
            data: bytes, content_type: str,
            media_name: str = None,
            sort_index: int = None,
    ) -> Tuple[MediaResource | None, SQLAlchemyError | None]:
        try:
            res = await self.oss_client.check_bucket_exists(bucket)
            if res is not None:
                return None, Exception(f"Bucket '{bucket}' does not exist")

            if media_name is None or media_name == '':
                object_name = f"object_{datetime.now().timestamp()}"
            else:
                object_name = media_name

            info = self.oss_client.save(
                bucket, object_name, data, len(data),
                content_type=content_type)

            url = f"{bucket}/{object_name}"
            if info.location != '':
                url = info.location

            return MediaResource(
                tenant_uuid=user.tenant_owner_uuid,
                created_user_by=user.uuid,
                bucket_name=bucket,
                filename=info.object_name,
                size=len(data),
                url=url,
                content_type=content_type,
                resource_type=get_media_type(content_type),
                sort_index=sort_index,
            ), None
        except Exception as e:
            return None, e

    async def check_bucket_exists(self, bucket: str) -> SQLAlchemyError | None:
        return await self.oss_client.check_bucket_exists(bucket)

    @classmethod
    def determine_content_type(cls, base64_data: str) -> str:
        # 通过前缀判断内容类型
        content_type = get_content_type_from_base64(base64_data)
        if content_type:
            return content_type
        # 如果没有前缀，使用魔术字节判断内容类型
        return get_file_type_from_magic_numbers(base64_data)
