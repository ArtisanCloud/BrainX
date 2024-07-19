from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dataset
from app.service.rag.dataset.service import DatasetService


async def get_dataset_by_uuid(
        db: AsyncSession,
        dataset_uuid: str
) -> Tuple[Dataset | None, Exception | None]:
    service_dataset = DatasetService(db)
    dataset, exception = service_dataset.app_dao.get_by_uuid(dataset_uuid)

    return dataset, exception
