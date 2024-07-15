from typing import Tuple
from app.models.app.app_model_config import AppModelConfig
from app.dao.app.app_model_config import AppModelConfigDAO
from app.schemas.app_model_config import AppModelConfigSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class AppModelConfigService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.app_model_config_dao = AppModelConfigDAO(self.db)

    async def create_app_model_config(self, config_data: AppModelConfigSchema) -> Tuple[
        AppModelConfig | None, Exception | None]:
        try:
            return await self.app_model_config_dao.create_app_model_config(config_data)
        except SQLAlchemyError as e:
            return None, e

    async def get_app_model_config_by_id(self, config_id: int) -> Tuple[
        AppModelConfig | None, Exception | None]:
        try:
            return await self.app_model_config_dao.get_app_model_config_by_id(config_id)
        except SQLAlchemyError as e:
            return None, e

    async def update_app_model_config(self, config_id: int, update_data: AppModelConfigSchema) -> Tuple[
        AppModelConfig | None, Exception | None]:
        try:
            return await self.app_model_config_dao.update_app_model_config(config_id, update_data)
        except SQLAlchemyError as e:
            return None, e

    async def patch_app_model_config(self, config_id: int, patch_data: dict) -> Tuple[
        AppModelConfig | None, Exception]:
        try:
            return await self.app_model_config_dao.patch_app_model_config(config_id, patch_data)
        except SQLAlchemyError as e:
            return None, e

    async def delete_app_model_config(self, config_id: int) -> Tuple[bool, Exception | None]:
        try:
            return await self.app_model_config_dao.delete_app_model_config(config_id)
        except SQLAlchemyError as e:
            return False, e
