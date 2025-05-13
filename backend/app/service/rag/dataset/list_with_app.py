from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.dataset import DatasetSchema
from app.service.rag.dataset.service import DatasetService, transform_datasets_with_app_to_reply


async def get_dataset_list_with_connected_app(
   async_db: AsyncSession,
    tenant_uuid: str,
    app_uuid: str,
    only_connected: bool,
) -> Tuple[List[DatasetSchema] | None, SQLAlchemyError | None]:
    dataset_service = DatasetService(async_db)

    # 只需要关联过app的dataset
    filter_by_app_uuid = None
    if only_connected:
        filter_by_app_uuid = app_uuid

    dataset_list, exception = (
        await dataset_service.dataset_dao.get_dataset_list_with_connected_app(
            tenant_uuid=tenant_uuid,
            app_uuid=filter_by_app_uuid,
        )
    )

    if exception:
        return None, exception

    return transform_datasets_with_app_to_reply(dataset_list, app_uuid), None
