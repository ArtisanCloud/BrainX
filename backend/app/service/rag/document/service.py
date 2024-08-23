from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.rag.dataset import DatasetDAO
from app.dao.rag.document import DocumentDAO
from app.logger import logger
from app.models import Dataset, Document, DatasetSegmentRule
from app.schemas.rag.document import RuleSchema


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.dataset_dao = DatasetDAO(db)
        self.document_dao = DocumentDAO(db)

    async def add_content(self, segment_rule: DatasetSegmentRule, documents: List[Document]):

        try:
            # 先创建分割规则
            if segment_rule is not None:
                segment_rule, exception = await self.dataset_dao.create(segment_rule)
                if exception is not None:
                    return None, None, exception

            # 创建文档
            documents, exception = await self.document_dao.create_many(documents)
            if exception is not None:
                return None, None, exception

            return segment_rule, documents, None

        except SQLAlchemyError as e:
            logger.error("捕获到SQLAlchemyError异常:", e)
            return None, None, e
