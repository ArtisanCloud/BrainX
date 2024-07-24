from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.rag.document import DocumentSchema

from app.service.base import paginate_query
from app.service.rag.document.create import transform_document_to_reply

from app.models.rag.document import Document


def transform_documents_to_reply(documents: [Document]) -> List[DocumentSchema]:
    data = [transform_document_to_reply(resource) for resource in documents]
    # print(data)
    return data


async def get_document_list(
        db: AsyncSession,
        tenant_uuid: str,
        dataset_uuid: str,
        pagination: Pagination
) -> Tuple[List[DocumentSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(Document).
        where(Document.tenant_uuid == tenant_uuid).
        where(Document.dataset_uuid == dataset_uuid).
        where(Document.deleted_at.is_(None)).
        order_by(Document.created_at).
        options(
            # joinedload(Document.dataset),  # 立即加载 dataset 关联
            subqueryload(Document.document_segments)  # 立即加载 document_segments 关联
        )
    )
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, Document, pagination, True)
    if exception:
        return None, None, exception

    return transform_documents_to_reply(res), pg, None
