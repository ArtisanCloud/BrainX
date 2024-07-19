from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.rag.document_segment import DocumentSegmentSchema

from app.service.base import paginate_query
from app.service.rag.dataset.create import transform_dataset_to_reply

from app.models.rag.document_segment import DocumentSegment


def transform_datasets_to_reply(document_segments: [DocumentSegment]) -> List[DocumentSegmentSchema]:
    data = [transform_dataset_to_reply(resource) for resource in document_segments]
    # print(data)
    return data


async def get_document_segment_list(
        db: AsyncSession,
        pagination: Pagination
) -> Tuple[List[DocumentSegmentSchema] | None, ResponsePagination | None, SQLAlchemyError | None]:
    stmt = (
        select(DocumentSegment).
        where(DocumentSegment.deleted_at.is_(None)).
        order_by(DocumentSegment.created_at)
    )
    # print(stmt)
    res, pg, exception = await paginate_query(db, stmt, DocumentSegment, pagination, True)
    if exception:
        return None, None, exception

    return transform_datasets_to_reply(res), pg, None