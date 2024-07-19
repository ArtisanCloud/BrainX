from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.dataset import DatasetSchema
from app.service.rag.dataset.create import transform_dataset_to_reply
from app.service.rag.dataset.service import DatasetService


async def patch_dataset(
        db: AsyncSession,
        dataset_uuid: str,
        update_data: Dict[str, Any]
) -> Tuple[DatasetSchema | None, Exception | None]:
    service_dataset = DatasetService(db)
    dataset, exception = await service_dataset.dataset_dao.patch(dataset_uuid, update_data)

    if exception:
        return None, exception

    return transform_dataset_to_reply(dataset), None
