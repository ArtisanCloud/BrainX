from typing import List, Tuple, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.dataset import DatasetDAO


class DatasetService:
    def __init__(self, db: AsyncSession):
        self.app_dao = DatasetDAO(db)

    async def sync_dataset_with_apps(
            self,
            app_uuid: str,
            connect_app_uuids: List[str],
            disconnect_app_uuids: List[str]
    ) -> Tuple[List[str] | None, SQLAlchemyError | None]:
        try:

            exception = await self.app_dao.sync_app_with_datasets(app_uuid, connect_app_uuids, disconnect_app_uuids)
            if exception:
                raise exception

            dataset_list, exception = await self.app_dao.get_connected_datasets(app_uuid)
            return dataset_list, exception

        except SQLAlchemyError as e:
            return None, e

    async def connect_dataset_with_apps(
            self,
            app_uuid: str,
            connect_app_uuids: List[str],
    ) -> SQLAlchemyError | None:
        try:

            exception = await self.app_dao.connect_datasets(app_uuid, connect_app_uuids)
            if exception:
                raise exception

        except SQLAlchemyError as e:
            return e

    async def disconnect_dataset_with_apps(
            self,
            app_uuid: str,
            dataset_uuids: List[str]
    ) -> SQLAlchemyError | None:
        try:

            exception = await self.app_dao.disconnect_datasets(app_uuid, dataset_uuids)
            if exception:
                raise exception

        except SQLAlchemyError as e:
            return e
