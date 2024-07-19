from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.rag.document.service import DocumentService


async def soft_delete_document(
        db: AsyncSession,
        user_id: int,
        document_uuid: str
) -> Tuple[bool | None, Exception | None]:
    service_document = DocumentService(db)
    result, exception = await service_document.soft_delete_document(user_id, document_uuid)

    if exception:
        return False, exception

    return result, None
