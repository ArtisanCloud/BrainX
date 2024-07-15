from datetime import datetime
from typing import Tuple, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.models.app.app import App


class AppDAO(BaseDAO[App]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, App)

    async def create_app(self, app: App) -> App:
        try:
            self.db.add(app)
            await self.db.commit()
            await self.db.refresh(app)
            return app
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    # async def create_apps(self, apps: List[App]) -> List[App]:
    #     try:
    #         self.db.add_all(apps)
    #         await self.db.commit()
    #         for app in apps:
    #             await self.db.refresh(app)
    #         return apps
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         raise e
    #
    async def patch_app(self, app_uuid: str, update_data: Dict[str, Any]) -> Tuple[App | None, SQLAlchemyError | None]:
        try:
            result = await self.db.execute(select(App).filter_by(uuid=app_uuid))
            exist_app = result.scalars().first()

            if exist_app is None:
                raise Exception("App not found")

            for field, value in update_data.items():
                setattr(exist_app, field, value)
            # 更新 `updated_at` 字段
            setattr(exist_app, "updated_at", datetime.now())


            await self.db.commit()
            await self.db.refresh(exist_app)

            return exist_app, None

        except SQLAlchemyError as e:
            await self.db.rollback()  # 确保在发生异常时回滚事务
            return None, SQLAlchemyError(f"patch app failed: {str(e)}")
    #
    # async def update_app(self, app: App) -> App:
    #     try:
    #         await self.db.commit()
    #         await self.db.refresh(app)
    #         return app
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         raise e
    #
    # async def get_app_by_uuid(self, app_uuid: str) -> App:
    #     try:
    #         result = await self.db.execute(select(App).filter_by(uuid=app_uuid))
    #         app = result.scalars().first()
    #         if app is None:
    #             raise Exception("App not found")
    #         return app
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         raise e
    #
    # async def soft_delete_app(self, user_id: int, app_uuid: str) -> Tuple[bool, Exception | None]:
    #     try:
    #         async with self.db() as session:
    #             sql = select(App).where(
    #                 and_(
    #                     App.uuid == app_uuid,
    #                     App.user_id == user_id
    #                 )
    #             )
    #             result = await session.execute(sql)
    #             exist_app = result.scalars().first()
    #
    #             if exist_app is None:
    #                 raise Exception("App not found")
    #
    #             exist_app.deleted_at = datetime.now()
    #             await session.commit()
    #             return True, None
    #
    #     except SQLAlchemyError as e:
    #         await session.rollback()  # 确保在发生异常时回滚事务
    #         raise SQLAlchemyError(f"soft delete app failed: {str(e)}")
    #
    # async def delete_app(self, user_id: int, app_uuid: str) -> Tuple[bool, Exception | None]:
    #     try:
    #         async with self.db() as session:
    #             delete_query = (
    #                 delete(App).
    #                 where(
    #                     and_(
    #                         App.uuid == app_uuid,
    #                         App.user_id == user_id
    #                     )
    #                 )
    #             )
    #             result = await session.execute(delete_query)
    #             rowcount = await result.scalar()
    #
    #             success = rowcount > 0
    #             await session.commit()
    #             return success, None
    #
    #     except SQLAlchemyError as e:
    #         await session.rollback()  # 确保在发生异常时回滚事务
    #         raise SQLAlchemyError(f"delete app failed: {str(e)}")
