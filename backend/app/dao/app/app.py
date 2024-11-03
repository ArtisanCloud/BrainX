from typing import Union, Tuple

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.app.app import App
from app.models.rag.pivot_app_to_dataset import PivotAppToDataset


class AppDAO(BaseDAO[App]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, App)

    async def get_app_by_uuid_with_preloads(self, app_uuid: str) -> Tuple[App | None, SQLAlchemyError | None]:
        # 构建查询语句，左连接 PivotAppToDataset 中的 Dataset 和 current_app_model_config
        try:
            query = (
                select(App)
                .where(App.uuid == app_uuid)
                .options(
                    # 使用 joinedload 预加载一对一关系的 current_app_model_config
                    joinedload(App.current_app_model_config),
                    # 使用 selectinload 预加载多对多关系的 connected_datasets
                    joinedload(App.connected_datasets),
                )
            )

            # print(query, app_uuid)

            # 执行查询并返回结果
            result = await self.db.execute(query)
            app = result.scalars().first()
            return app, None

        except SQLAlchemyError as e:
            return None, e
