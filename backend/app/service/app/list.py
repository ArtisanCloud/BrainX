from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.app.app import AppSchema
from app.service.app.service import transform_apps_to_reply

from app.service.base import paginate_query

from app.models.app.app import App


async def get_app_list(
   async_db: AsyncSession, tenant_uuid: str, pagination: Pagination
) -> Tuple[List[AppSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(App)
        .where(App.tenant_uuid == tenant_uuid)
        .where(App.deleted_at.is_(None))
        .options(
            # 使用 selectinload 预加载多对多关系的 connected_datasets
            joinedload(App.connected_datasets),
            # 使用 joinedload 预加载一对一关系的 current_app_model_config
            joinedload(App.current_app_model_config),
        )
        .order_by(App.created_at)
    )
    # print(stmt)
    res, pg, exception = await paginate_query(
        async_db, stmt, App, pagination, True, need_unique=True
    )
    if exception:
        return None, None, exception

    return transform_apps_to_reply(res), pg, None
