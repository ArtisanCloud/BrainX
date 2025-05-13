from typing import List, Tuple, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.dao.rag.dataset import DatasetDAO
from app.models.rag.dataset import Dataset
from app.schemas.rag.dataset import DatasetSchema


class DatasetService:
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        self.dataset_dao = DatasetDAO(async_db, sync_db)

    async def sync_dataset_with_apps(
        self,
        app_uuid: str,
        connect_app_uuids: List[str],
        disconnect_app_uuids: List[str],
    ) -> Tuple[List[str] | None, SQLAlchemyError | None]:
        try:

            exception = await self.dataset_dao.sync_app_with_datasets(
                app_uuid, connect_app_uuids, disconnect_app_uuids
            )
            if exception:
                raise exception

            dataset_list, exception = await self.dataset_dao.get_connected_datasets(
                app_uuid
            )
            return dataset_list, exception

        except SQLAlchemyError as e:
            return None, e

    async def connect_dataset_with_apps(
        self,
        app_uuid: str,
        connect_app_uuids: List[str],
    ) -> SQLAlchemyError | None:
        try:

            exception = await self.dataset_dao.connect_datasets(
                app_uuid, connect_app_uuids
            )
            if exception:
                raise exception

        except SQLAlchemyError as e:
            return e

    async def disconnect_dataset_with_apps(
        self, app_uuid: str, dataset_uuids: List[str]
    ) -> SQLAlchemyError | None:
        try:

            exception = await self.dataset_dao.disconnect_datasets(
                app_uuid, dataset_uuids
            )
            if exception:
                raise exception

        except SQLAlchemyError as e:
            return e


def transform_dataset_to_reply(dataset: Dataset) -> [DatasetSchema | None]:
    if dataset is None:
        return None

    return DatasetSchema.from_orm(dataset)


def transform_datasets_to_reply(datasets: [Dataset]) -> List[DatasetSchema]:
    data = [transform_dataset_to_reply(resource) for resource in datasets]
    # print(data)
    return data


def transform_datasets_with_app_to_reply(
    datasets: [Dataset], app_uuid: str
) -> List[DatasetSchema]:
    data = [
        transform_dataset_with_app_to_reply(resource, app_uuid) for resource in datasets
    ]
    # print(data)
    return data


def transform_dataset_with_app_to_reply(
    dataset: Dataset, app_uuid: str
) -> DatasetSchema:
    data = DatasetSchema.from_orm(dataset)
    data.with_app_connected = any(
        str(app.app_uuid) == app_uuid for app in dataset.connected_app_pivots
    )
    return data
