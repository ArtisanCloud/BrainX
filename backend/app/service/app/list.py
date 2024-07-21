from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.app.app import AppSchema

from app.service.base import paginate_query
from app.service.app.create import transform_app_to_reply

from app.models.app.app import App


def transform_apps_to_reply(apps: [App]) -> List[AppSchema]:
    data = [transform_app_to_reply(resource) for resource in apps]
    # print(data)
    return data


async def get_app_list(
        db: AsyncSession,
        tenant_uuid: str,
        pagination: Pagination
) -> Tuple[List[AppSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(App).
        where(App.tenant_uuid == tenant_uuid).
        where(App.deleted_at.is_(None)).
        order_by(App.created_at)
    )
    print(stmt)
    res, pg, exception = await paginate_query(db, stmt, App, pagination, True)
    if exception:
        return None, None, exception

    return transform_apps_to_reply(res), pg, None
