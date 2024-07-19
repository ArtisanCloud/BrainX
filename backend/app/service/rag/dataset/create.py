from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.dataset import DatasetSchema
from app.service.rag.dataset.service import DatasetService

from app.models.rag.dataset import Dataset


def transform_dataset_to_reply(dataset: Dataset) -> [DatasetSchema | None]:
    if dataset is None:
        return None

    return DatasetSchema.from_orm(dataset)


async def create_dataset(
        db: AsyncSession,
        dataset: Dataset,
) -> Tuple[DatasetSchema | None, Exception | None]:
    service_dataset = DatasetService(db)
    dataset, exception = await service_dataset.app_dao.create(dataset)

    if exception:
        return None, exception

    return transform_dataset_to_reply(dataset), None
