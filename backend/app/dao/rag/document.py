from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models import User
from app.models.rag.document import Document, DocumentIndexingStatus
from datetime import datetime, timezone


class DocumentDAO(BaseDAO[Document]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Document)

    async def set_indexing_status(self, document: Document,
                                  status: DocumentIndexingStatus,
                                  error=None,
                                  user: User = None) -> Tuple[
        Optional[Document], Optional[SQLAlchemyError]]:
        try:
            # 检索文档对象
            if not document:
                return None, None  # 文档未找到

            # 更新 status 和 updated_user_by
            document.status = status
            if user:
                document.updated_user_by = user.uuid

            # 获取带有 UTC 时区信息的当前时间
            current_time = datetime.now(timezone.utc)
            document.updated_at = current_time

            # 根据状态更新不同的时间字段
            if status == DocumentIndexingStatus.PARSING:
                document.parse_start_at = current_time

            elif status == DocumentIndexingStatus.EXTRACTING:
                document.extract_start_at = current_time

            elif status == DocumentIndexingStatus.CLEANING:
                document.clean_start_at = current_time

            elif status == DocumentIndexingStatus.SPLITTING:
                document.split_start_at = current_time

            elif status == DocumentIndexingStatus.INDEXING:
                document.index_start_at = current_time

            elif status == DocumentIndexingStatus.COMPLETED:
                document.indexing_latency = (
                    current_time.timestamp() - document.parse_start_at.timestamp()
                    if document.parse_start_at else None
                )
                document.process_end_at = current_time

            elif status == DocumentIndexingStatus.PAUSE:
                document.paused_at = current_time
                if user:
                    document.paused_by = user.uuid

            elif status == DocumentIndexingStatus.ARCHIVED:
                document.paused_at = current_time
                if user:
                    document.archived_by = user.uuid

            elif status == DocumentIndexingStatus.ERROR:
                document.error_message = error
                document.error_at = current_time


            # 刷新并保存
            await self.db.flush()
            await self.db.refresh(document)

            return document, None

        except SQLAlchemyError as e:
            return None, e
