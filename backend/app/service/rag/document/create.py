from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.document import DocumentSchema
from app.service.rag.document.service import (
    DocumentService,
    transform_document_to_reply,
)

from app.models.rag.document import Document


async def create_document(
   async_db: AsyncSession,
    document: Document,
) -> Tuple[DocumentSchema | None, Exception | None]:
    service_document = DocumentService(async_db)
    document, exception = await service_document.document_dao.async_create(document)

    if exception:
        return None, exception

    return transform_document_to_reply(document), None
