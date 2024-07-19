from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.document import DocumentSchema
from app.service.rag.document.create import transform_document_to_reply
from app.service.rag.document.service import DocumentService


async def patch_document(
        db: AsyncSession,
        document_uuid: str,
        update_data: Dict[str, Any]
) -> Tuple[DocumentSchema | None, Exception | None]:
    service_document = DocumentService(db)
    document, exception = await service_document.document_dao.patch(document_uuid, update_data)

    if exception:
        return None, exception

    return transform_document_to_reply(document), None
