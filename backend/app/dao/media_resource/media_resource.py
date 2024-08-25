from typing import Union

from sqlalchemy.orm import Session
import mimetypes
from typing import List, Tuple

from app.dao.base import BaseDAO
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.media_resource.model import MediaResource
from app.schemas.base import ResponsePagination, Pagination
from app.service.base import paginate_query


def get_media_type(content_type: str) -> str:
    return mimetypes.guess_extension(content_type)


class FindManyMediaResourcesOption(BaseModel):
    ids: List[int]
    uuids: List[str]
    like_name: str
    types: List[str]
    page_embed_option: Pagination  # Assuming PageEmbedOption is a defined class


bucket_media_resource_product = "bucket.brainx"

DEFAULT_STORAGE_PATH = "public/static"


class MediaResourceDAO(BaseDAO[MediaResource]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, MediaResource)

    async def build_find_query_no_page(self, query: select, opt: FindManyMediaResourcesOption) -> select:
        if opt.ids:
            query = query.where(MediaResource.c.id.in_(opt.ids))
        if opt.uuids:
            query = query.where(MediaResource.c.uuid.in_(opt.uuids))

        if opt.types:
            query = query.where(MediaResource.media_type.in_(opt.types))

        if opt.like_name:
            query = query.where(MediaResource.c.filename.like(f"%{opt.like_name}%"))

        return query

    async def find_all_media_resources(self) -> Tuple[List[MediaResource], SQLAlchemyError]:
        try:
            result = await self.db.execute(select(MediaResource))
            return result.scalars().all(), None
        except SQLAlchemyError as e:
            return [], e

    async def find_many_media_resources(
            self, opt: FindManyMediaResourcesOption
    ) -> Tuple[List[MediaResource] | None, ResponsePagination | None, SQLAlchemyError | None]:
        try:
            stmt = select(MediaResource)
            stmt = await self.build_find_query_no_page(stmt, opt)
            return await paginate_query(self.db, stmt, opt.page_embed_option, True)
        except SQLAlchemyError as e:
            return None, None, e

    async def create_media_resource(self, resource: MediaResource) -> Tuple[MediaResource | None, SQLAlchemyError | None]:
        try:
            self.db.add(resource)

            await self.db.flush()
            await self.db.refresh(resource)
            return resource, None
        except SQLAlchemyError as e:

            return None, e

    async def create_media_resources(
            self, resources: List[MediaResource]
    ) -> Tuple[List[MediaResource] | None, SQLAlchemyError | None]:
        try:
            self.db.add_all(resources)
            await self.db.flush()

            return resources, None
        except SQLAlchemyError as e:

            return None, e
