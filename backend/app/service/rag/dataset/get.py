from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dataset, User
from app.service.rag.dataset.create import transform_dataset_to_reply
from app.service.rag.dataset.service import DatasetService


async def get_dataset_by_uuid(
        db: AsyncSession,
        user: User,
        dataset_uuid: str
) -> Tuple[Dataset | None, Exception | None]:
    service_dataset = DatasetService(db)
    dataset, exception = await service_dataset.app_dao.get_by_uuid(dataset_uuid)

    #
    if exception:
        return None, exception

    #
    if dataset is None:
        return None, Exception("object not found")

    # check if the dataset is belong to the user's tenant
    if dataset.tenant_uuid != user.tenant_owner_uuid:
        return None, Exception("Object is not belong to your owned tenant")

    return transform_dataset_to_reply(dataset), None
