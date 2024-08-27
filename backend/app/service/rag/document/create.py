from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rag.document import DocumentSchema
from app.service.rag.document.service import DocumentService

from app.models.rag.document import Document


def transform_document_to_reply(document: Document) -> [DocumentSchema | None]:
    if document is None:
        return None

    return DocumentSchema.from_orm(document)


async def create_document(
        db: AsyncSession,
        document: Document,
) -> Tuple[DocumentSchema | None, Exception | None]:
    service_document = DocumentService(db)
    document, exception = await service_document.document_dao.async_create(document)

    if exception:
        return None, exception

    return transform_document_to_reply(document), None
