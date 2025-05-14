from typing import Tuple, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.config.config import UTC

from app.dao.base import BaseDAO
from app.models import User
from app.models.rag.document import Document, DocumentIndexingStatus, DocumentStatus
from datetime import datetime


class DocumentDAO(BaseDAO[Document]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Document, async_db, sync_db)

    def _set_indexing_status(self, document: Document,
                             indexing_status: DocumentIndexingStatus,
                             error=None,
                             user: User = None) -> Tuple[Optional[Document], Optional[SQLAlchemyError]]:
        try:
            # 检索文档对象
            if not document:
                return None, None  # 文档未找到

            # 更新 status 和 updated_user_by
            document.indexing_status = indexing_status
            if user:
                document.updated_user_by = user.uuid

            # 获取带有 UTC 时区信息的当前时间
            current_time = datetime.now(UTC)
            document.updated_at = current_time

            # 根据状态更新不同的时间字段
            if indexing_status == DocumentIndexingStatus.PARSING:
                document.process_start_at = current_time
                document.parse_start_at = current_time

            elif indexing_status == DocumentIndexingStatus.EXTRACTING:
                document.extract_start_at = current_time

            elif indexing_status == DocumentIndexingStatus.CLEANING:
                document.clean_start_at = current_time

            elif indexing_status == DocumentIndexingStatus.SPLITTING:
                document.split_start_at = current_time

            elif indexing_status == DocumentIndexingStatus.INDEXING:
                document.index_start_at = current_time

            elif indexing_status == DocumentIndexingStatus.COMPLETED:
                document.indexing_latency = (
                    current_time.timestamp() - document.parse_start_at.timestamp()
                    if document.parse_start_at else None
                )
                document.process_end_at = current_time
                document.status = DocumentStatus.NORMAL

            elif indexing_status == DocumentIndexingStatus.PAUSE:
                document.paused_at = current_time
                if user:
                    document.paused_by = user.uuid

            elif indexing_status == DocumentIndexingStatus.ARCHIVED:
                document.paused_at = current_time
                if user:
                    document.archived_by = user.uuid

            elif indexing_status == DocumentIndexingStatus.ERROR:
                document.error_message = error
                document.error_at = current_time

            return document, None

        except SQLAlchemyError as e:
            print("error: ", e)
            return None, e

    async def async_set_indexing_status(self, document: Document,
                                        status: DocumentIndexingStatus,
                                        error=None,
                                        user: User = None) -> Tuple[Optional[Document], Optional[SQLAlchemyError]]:
        try:
            document, error = self._set_indexing_status(document, status, error, user)
            if error:
                return None, error
            await self.async_db.flush()
            await self.async_db.refresh(document)
            return document, None
        except SQLAlchemyError as e:
            print("error: ", e)
            return None, e

    def set_indexing_status(self, document: Document,
                            status: DocumentIndexingStatus,
                            error=None,
                            user: User = None) -> Tuple[Optional[Document], Optional[SQLAlchemyError]]:
        try:
            document, error = self._set_indexing_status(document, status, error, user)
            if error:
                return None, error
            self.sync_db.flush()
            self.sync_db.refresh(document)
            return document, None
        except SQLAlchemyError as e:
            print("error: ", e)
            return None, e

    def set_word_count(self, document: Document, word_count: int) -> Tuple[
        Optional[Document], Optional[SQLAlchemyError]]:
        try:
            document.word_count = word_count
            self.sync_db.flush()
            self.sync_db.refresh(document)
            return document, None
        except SQLAlchemyError as e:
            return None, e
