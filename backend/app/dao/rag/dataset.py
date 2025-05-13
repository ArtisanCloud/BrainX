from typing import Tuple, Union, List, Dict, Any, Sequence

from sqlalchemy.orm import Session, joinedload

from sqlalchemy import select, and_, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload

from app.dao.base import BaseDAO
from app.database.session_manager import is_dep_session
from app.logger import logger
from app.models import App
from app.models.rag.dataset import Dataset, DatasetSegmentRule
from app.models.rag.pivot_app_to_dataset import PivotAppToDataset


class DatasetDAO(BaseDAO[Dataset]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Dataset, async_db, sync_db)

    async def load_segment_rule(self, dataset: Dataset) -> Tuple[Dataset | None, SQLAlchemyError | None]:
        try:
            # segment = await dataset.awaitable_attrs.segment_rule  # 这行代码会触发懒加载
            # 检查是否已经加载过 segment_rule
            # if dataset.segment_rule is not None:
            #     return dataset, None

            # 手动查询 segment_rule
            result = await self.async_db.execute(
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

    async def get_dataset_list_with_connected_app(
            self,
            tenant_uuid: str,
            app_uuid: str = None,
    ) -> Tuple[Sequence[Dataset] | None, SQLAlchemyError | None]:
        try:
            stmt = (
                select(Dataset)
                .outerjoin(PivotAppToDataset, Dataset.uuid == PivotAppToDataset.dataset_uuid)
                .outerjoin(App, PivotAppToDataset.app_uuid == App.uuid)
                .where(Dataset.tenant_uuid == tenant_uuid)
                .where(Dataset.deleted_at.is_(None))
                .options(joinedload(Dataset.connected_app_pivots))  # 确保预加载
            )

            if app_uuid is not None:
                stmt = stmt.where(PivotAppToDataset.app_uuid == app_uuid)  # 只返回已关联的 dataset

            # 排序
            stmt = stmt.order_by(Dataset.created_at)

            result = await self.async_db.execute(stmt)
            rows = result.unique().scalars().all()
            return rows, None

        except SQLAlchemyError as e:
            return None, e

    async def sync_app_with_datasets(
            self,
            app_uuid: str,
            connect_database_uuids: List[str],
            disconnect_database_uuids: List[str],
            conditions: Dict[str, Any] = None
    ) -> SQLAlchemyError | None:
        try:
            # 创建新的 PivotAppToDataset 实例
            for dataset_uuid in connect_database_uuids:
                pivot_entry = PivotAppToDataset(app_uuid=app_uuid, dataset_uuid=dataset_uuid)
                self.async_db.add(pivot_entry)

            # 删除与指定 app_uuids 相关的 PivotAppToDataset 记录
            stmt = delete(PivotAppToDataset).where(
                PivotAppToDataset.dataset.in_(disconnect_database_uuids),
                PivotAppToDataset.app_uuid == app_uuid
            )
            await self.async_db.execute(stmt)
            return None
        except SQLAlchemyError as e:
            return e

    async def connect_datasets(
            self,
            app_uuid: str,
            connect_database_uuids: List[str],
            conditions: Dict[str, Any] = None
    ) -> SQLAlchemyError | None:
        try:
            # 创建新的 PivotAppToDataset 实例
            for dataset_uuid in connect_database_uuids:
                # 检查是否已存在关联
                exists = await self.async_db.execute(
                    select(PivotAppToDataset)
                    .where(PivotAppToDataset.app_uuid == app_uuid)
                    .where(PivotAppToDataset.dataset_uuid == dataset_uuid)
                )
                # 如果不存在则插入
                if not exists.scalars().first():
                    pivot_entry = PivotAppToDataset(app_uuid=app_uuid, dataset_uuid=dataset_uuid)
                    self.async_db.add(pivot_entry)

            return None
        except SQLAlchemyError as e:
            return e

    async def disconnect_datasets(
            self,
            app_uuid: str,
            dataset_uuids: List[str],
            conditions: Dict[str, Any] = None
    ) -> SQLAlchemyError | None:
        try:
            # 删除与指定 app_uuids 相关的 PivotAppToDataset 记录
            stmt = delete(PivotAppToDataset).where(
                PivotAppToDataset.dataset_uuid.in_(dataset_uuids),
                PivotAppToDataset.app_uuid == app_uuid
            )
            await self.async_db.execute(stmt)
            if not is_dep_session(self.async_db):
                await self.async_db.commit()

            return None
        except SQLAlchemyError as e:
            if not is_dep_session(self.async_db):
                await self.async_db.rollback()
            return e

    async def get_connected_datasets(self, app_uuid: str) -> Tuple[Sequence[Dataset] | None, SQLAlchemyError | None]:
        try:
            stmt = (
                select(Dataset)
                .join(PivotAppToDataset, Dataset.uuid == PivotAppToDataset.dataset_uuid)
                .where(PivotAppToDataset.app_uuid == app_uuid)
            )
            result = await self.async_db.execute(stmt)
            datasets = result.scalars().all()
            return datasets, None

        except SQLAlchemyError as e:
            return None, e
