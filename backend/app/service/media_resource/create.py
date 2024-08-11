from typing import Tuple

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.media_resource.media_resource import bucket_media_resource_product
from app.models import User
from app.models.media_resource.model import MediaResource
from app.schemas.media_resource.schema import MediaResourceSchema
from app.service.media_resource.service import MediaResourceService
from app.utils.datetime import datetime_format


def transform_media_resource_to_reply(resource: MediaResource) -> [MediaResourceSchema | None]:
    if resource is None:
        return None

    return MediaResourceSchema.from_orm(resource)


async def create_media_resource_by_file(
        db: AsyncSession,
        handler: UploadFile,
) -> Tuple[MediaResourceSchema | None, Exception | None]:
    # Create media resource
    service_media_resource = MediaResourceService(db)
    media_resource, exception = await service_media_resource.make_media_resource(bucket_media_resource_product, handler)
    if exception:
        return None, exception

    media_resource, exception = await service_media_resource.create_media_resource(media_resource)
    if exception:
        return None, Exception(f"Database error: {exception}")

    # print(media_resource, exception)
    return transform_media_resource_to_reply(media_resource), None


async def create_media_resource_by_base64_string(
        db: AsyncSession, user: User,
        bucket: str, base64_data: str,
        media_name: str = None, sort_index: int = None,
) -> Tuple[MediaResourceSchema | None, Exception | None]:
    # Create media resource
    service_media_resource = MediaResourceService(db)
    media_resource, exception = await service_media_resource.make_oss_resource_by_base64_string(
        user, bucket, base64_data, media_name, sort_index)
    if exception:
        return None, exception

    media_resource, exception = await service_media_resource.create_media_resource(media_resource)
    if exception:
        return None, Exception(f"Database error: {exception}")
    print(123321, media_resource, exception)
    return transform_media_resource_to_reply(media_resource), None
