from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document, User
from app.service.rag.document.create import transform_document_to_reply
from app.service.rag.document.service import DocumentService


async def get_document_by_uuid(
        db: AsyncSession,
        user: User,
        document_uuid: str
) -> Tuple[Document | None, Exception | None]:
    service_document = DocumentService(db)
    document, exception = await (service_document.
                                 document_dao.
                                 get_by_uuid(document_uuid))

    #
    if exception:
        return None, exception

    #
    if document is None:
        return None, Exception("object not found")

    # check if the document is belong to the user's tenant
    if document.tenant_uuid != user.tenant_owner_uuid:
        return None, Exception("Object is not belong to your owned tenant")

    return transform_document_to_reply(document), None
