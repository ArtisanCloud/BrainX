from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.media_resource.model import MediaResource
from app.schemas.base import Pagination, ResponsePagination
from app.schemas.media_resource.schema import MediaResourceSchema
from app.service.base import paginate_query
from app.service.media_resource.service import transform_media_resources_to_reply


async def get_media_resource_list(
    db: AsyncSession, pagination: Pagination
) -> Tuple[
    List[MediaResource] | None, ResponsePagination | None, SQLAlchemyError | None
]:
    stmt = select(MediaResource)
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, MediaResource, pagination, True)
    if exception:
        return None, None, exception

    return transform_media_resources_to_reply(res), pg, None
