from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.media_resource.model import MediaResource
from app.schemas.base import Pagination, ResponsePagination
from app.schemas.media_resource.schema import MediaResourceSchema
from app.service.base import paginate_query


def transform_media_resources_to_reply(media_resources: [MediaResource]) -> List[MediaResource]:
    data = [transform_media_resource_to_reply(resource) for resource in media_resources]
    return data


def transform_media_resource_to_reply(media_resource: MediaResource) -> MediaResourceSchema:
    return MediaResourceSchema(
        filename=media_resource.filename,
        size=media_resource.size,
        width=media_resource.width,
        height=media_resource.height,
        url=media_resource.url,
        bucket_name=media_resource.bucket_name,
        is_local_stored=media_resource.is_local_stored,
        content_type=media_resource.content_type,
        resource_type=media_resource.resource_type,
    )


async def get_media_resource_list(
        db: AsyncSession,
        pagination: Pagination
) -> Tuple[List[MediaResource] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = select(MediaResource)
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, MediaResource, pagination, True)
    if exception:
        return None, None, exception

    return transform_media_resources_to_reply(res), pg, None
