from typing import Tuple, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.base import Pagination, ResponsePagination
from app.schemas.rag.document_segment import DocumentSegmentSchema

from app.service.base import paginate_query

from app.models.rag.document_segment import DocumentSegment
from app.service.rag.document_segment.service import (
    transform_document_segments_to_reply,
)


async def get_document_segment_list(async_db: AsyncSession, pagination: Pagination) -> Tuple[
    List[DocumentSegmentSchema] | None,
    ResponsePagination | None,
    SQLAlchemyError | None,
]:
    stmt = (
        select(DocumentSegment)
        .where(DocumentSegment.deleted_at.is_(None))
        .order_by(DocumentSegment.created_at)
    )
    # print(stmt)
    res, pg, exception = await paginate_query(
        async_db, stmt, DocumentSegment, pagination, True
    )
    if exception:
        return None, None, exception

    return transform_document_segments_to_reply(res), pg, None
