from typing import Tuple, Dict, Any, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.app import AppDAO
from app.models.app import App


class AppService:
    def __init__(self, db: AsyncSession):
        self.app_dao = AppDAO(db)

    async def create_app(self, app_data: Dict[str, Any]) -> Tuple[App | None, Exception | None]:
        try:
            app = App(**app_data)
            created_app = await self.app_dao.create_app(app)
            return created_app, None
        except SQLAlchemyError as e:
            return None, e

    async def create_apps(self, apps_data: List[Dict[str, Any]]) -> Tuple[List[App] | None, Exception | None]:
        try:
            apps = [App(**data) for data in apps_data]
            created_apps = await self.app_dao.create_apps(apps)
            return created_apps, None
        except SQLAlchemyError as e:
            return None, e

    async def patch_app(self, app_uuid: str, update_data: Dict[str, Any]) -> Tuple[App | None, Exception | None]:
        try:
            updated_app, exception = await self.app_dao.patch(app_uuid, update_data)
            return updated_app, exception
        except SQLAlchemyError as e:
            return None, e

    async def get_app_by_uuid(self, app_uuid: str) -> Tuple[App | None, Exception | None]:
        try:
            app, exception = await self.app_dao.get_by_uuid(app_uuid)
            if exception:
                return None, exception
            return app, None
        except SQLAlchemyError as e:
            return None, e

    async def soft_delete_app(self, user_id: int, app_uuid: str) -> Tuple[bool, Exception | None]:
        try:
            success, error = await self.app_dao.soft_delete_app(user_id, app_uuid)
            return success, error
        except SQLAlchemyError as e:
            return False, e

    async def delete_app(self, user_id: int, app_uuid: str) -> Tuple[bool, Exception | None]:
        try:
            success, error = await self.app_dao.delete_app(user_id, app_uuid)
            return success, error
        except SQLAlchemyError as e:
            return False, e
