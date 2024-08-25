from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.app.app_model_config import AppModelConfig
from typing import Tuple
from app.schemas.app.app_model_config import AppModelConfigSchema


class AppModelConfigDAO:
    def __init__(self, db: Union[AsyncSession, Session]):
        self.db = db

    async def create_app_model_config(self, config_data: AppModelConfigSchema) -> Tuple[
        AppModelConfig | None, SQLAlchemyError | None]:
        try:
            app_model_config = AppModelConfig(**config_data.dict())
            self.db.add(app_model_config)

            return app_model_config, None
        except SQLAlchemyError as e:

            return None, e

    async def get_app_model_config_by_id(self, config_id: int) -> Tuple[
        AppModelConfig | None, SQLAlchemyError | None]:
        try:
            app_model_config = await self.db.execute(
                select(AppModelConfig).filter(AppModelConfig.id == config_id)
            )
            return app_model_config.scalar_one_or_none(), None
        except SQLAlchemyError as e:
            return None, e

    async def update_app_model_config(self, config_id: int, update_data: AppModelConfigSchema) \
            -> Tuple[AppModelConfig | None, SQLAlchemyError | None]:
        try:
            app_model_config = await self.get_app_model_config_by_id(config_id)
            if not app_model_config:
                return None, Exception(f"AppModelConfig with id {config_id} not found")

            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(app_model_config, field, value)

            return app_model_config, None
        except SQLAlchemyError as e:

            return None, e

    async def patch_app_model_config(self, config_id: int, patch_data: dict) -> Tuple[
        AppModelConfig | None, Exception]:
        try:
            app_model_config = await self.get_app_model_config_by_id(config_id)
            if not app_model_config:
                return None, Exception(f"AppModelConfig with id {config_id} not found")

            for field, value in patch_data.items():
                setattr(app_model_config, field, value)

            return app_model_config, None
        except SQLAlchemyError as e:
            return None, e

    async def delete_app_model_config(self, config_id: int) -> Tuple[bool, SQLAlchemyError | None]:
        try:
            app_model_config = await self.get_app_model_config_by_id(config_id)
            if not app_model_config:
                return False, Exception(f"AppModelConfig with id {config_id} not found")

            await self.db.delete(app_model_config)

            return True, None
        except SQLAlchemyError as e:

            return False, e
