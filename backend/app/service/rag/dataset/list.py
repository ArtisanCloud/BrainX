from typing import Tuple, List, Dict, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.rag.dataset import DatasetSchema

from app.service.base import paginate_query
from app.service.rag.dataset.create import transform_dataset_to_reply

from app.models.rag.dataset import Dataset


async def get_dataset_list(
    db: AsyncSession,
    tenant_uuid: str,
    pagination: Pagination,
    conditions: Dict[str, Any] = None,
) -> Tuple[
    List[DatasetSchema] | None, ResponsePagination | None, SQLAlchemyError | None
]:
    stmt = (
        select(Dataset)
        .where(Dataset.tenant_uuid == tenant_uuid)
        .where(Dataset.deleted_at.is_(None))
    )
    # print(str(stmt), tenant_uuid)
    if conditions:
        # 生成动态的 where 子句
        stmt = stmt.where(
            and_(
                *(
                    getattr(Dataset, field) == value
                    for field, value in conditions.items()
                    if value is not None
                )
            )
        )
    # 排序
    stmt = stmt.order_by(Dataset.created_at)

    res, pg, exception = await paginate_query(db, stmt, Dataset, pagination, True)
    if exception:
        return None, None, exception

    return transform_datasets_to_reply(res), pg, None
