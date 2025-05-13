from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.document_segment import DocumentSegmentSchema
from app.service.rag.dataset.create import transform_dataset_to_reply
from app.service.rag.dataset.service import DatasetService


async def patch_document(
       async_db: AsyncSession,
        document_uuid: str,
        update_data: Dict[str, Any]
) -> Tuple[DocumentSegmentSchema | None, Exception | None]:
    service_document = DatasetService(async_db)
    document, exception = await service_document.document_dao.patch(document_uuid, update_data)

    if exception:
        return None, exception

    return transform_dataset_to_reply(document), None
