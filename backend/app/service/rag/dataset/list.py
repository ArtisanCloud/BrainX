from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.rag.dataset import DatasetSchema

from app.service.base import paginate_query
from app.service.rag.dataset.create import transform_dataset_to_reply

from app.models.rag.dataset import Dataset


def transform_datasets_to_reply(datasets: [Dataset]) -> List[DatasetSchema]:
    data = [transform_dataset_to_reply(resource) for resource in datasets]
    # print(data)
    return data


async def get_dataset_list(
        db: AsyncSession,
        tenant_uuid: str,
        pagination: Pagination
) -> Tuple[List[DatasetSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(Dataset).
        where(Dataset.tenant_uuid == tenant_uuid).
        where(Dataset.deleted_at.is_(None)).
        order_by(Dataset.created_at)
    )
    # print(str(stmt))
    res, pg, exception = await paginate_query(db, stmt, Dataset, pagination, True)
    if exception:
        return None, None, exception

    return transform_datasets_to_reply(res), pg, None
