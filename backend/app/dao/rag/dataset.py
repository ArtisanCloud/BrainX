from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload

from app.dao.base import BaseDAO
from app.logger import logger
from app.models.rag.dataset import Dataset, DatasetSegmentRule


class DatasetDAO(BaseDAO[Dataset]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Dataset)

    async def load_segment_rule(self, dataset: Dataset) -> Tuple[Dataset | None, SQLAlchemyError | None]:
        try:
            # segment = await dataset.awaitable_attrs.segment_rule  # 这行代码会触发懒加载
            # 检查是否已经加载过 segment_rule
            # if dataset.segment_rule is not None:
            #     return dataset, None

            # 手动查询 segment_rule
            result = await self.db.execute(
                select(DatasetSegmentRule).where(DatasetSegmentRule.dataset_uuid == dataset.uuid)
            )
            segment_rule = result.scalars().first()

            # 将查询结果赋值给 dataset.segment_rule
            dataset.segment_rule = segment_rule
            # print(segment_rule)
            return dataset, None

        except SQLAlchemyError as e:
            logger.error("捕获到SQLAlchemyError异常:", e)

            return None, e
