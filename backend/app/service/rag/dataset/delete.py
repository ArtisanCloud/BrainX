from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.rag.dataset.service import DatasetService


async def soft_delete_dataset(
        db: AsyncSession,
        user_id: int,
        dataset_uuid: str
) -> Tuple[bool | None, Exception | None]:
    service_dataset = DatasetService(db)
    result, exception = await service_dataset.app_dao.soft_delete(user_id, dataset_uuid)

    if exception:
        return False, exception

    return result, None
