from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.dataset import DatasetSchema
from app.service.rag.dataset.service import DatasetService, transform_dataset_to_reply

from app.models.rag.dataset import Dataset


async def create_dataset(
    db: AsyncSession,
    dataset: Dataset,
) -> Tuple[DatasetSchema | None, Exception | None]:
    service_dataset = DatasetService(db)
    dataset, exception = await service_dataset.dataset_dao.async_create(dataset)
    if exception:
        return None, exception

    return transform_dataset_to_reply(dataset), None
