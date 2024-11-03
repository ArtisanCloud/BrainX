from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.app.app import AppSchema

from app.service.base import paginate_query
from app.service.app.create import transform_app_to_reply

from app.models.app.app import App


def transform_apps_to_reply(apps: [App]) -> List[AppSchema]:
    data = [transform_app_to_reply(app) for app in apps]
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
        options(
            # 使用 selectinload 预加载多对多关系的 connected_datasets
            # selectinload(App.connected_datasets),
            # 使用 joinedload 预加载一对一关系的 current_app_model_config
            joinedload(App.current_app_model_config)
        ).
        order_by(App.created_at)
    )
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, App, pagination, True)
    if exception:
        return None, None, exception

    return transform_apps_to_reply(res), pg, None
