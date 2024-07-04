from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.model_provider import ModelProvider
from typing import Tuple
from app.schemas.model_provider import ModelProviderSchema
from app.dao.base import BaseDAO


class ModelProviderDAO(BaseDAO[ModelProvider]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ModelProvider)

    # async def create_model_provider(self, provider_data: ModelProviderSchema) -> Tuple[
    #     ModelProvider | None, Exception | None]:
    #     try:
    #         model_provider = ModelProvider(**provider_data.dict())
    #         self.db.add(model_provider)
    #         await self.db.commit()
    #         return model_provider, None
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         return None, e
    #
    # async def get_model_provider_by_uuid(self, provider_uuid: str) -> Tuple[ModelProvider | None, Exception | None]:
    #     try:
    #         model_provider = await self.db.execute(
    #             select(ModelProvider).filter(ModelProvider.uuid == provider_uuid)
    #         )
    #         return model_provider.scalar_one_or_none(), None
    #     except SQLAlchemyError as e:
    #         return None, e
    #
    # async def update_model_provider(self, provider_uuid: str, update_data: ModelProviderSchema) \
    #         -> Tuple[ModelProvider | None, Exception | None]:
    #     try:
    #         model_provider = await self.get_model_provider_by_uuid(provider_uuid)
    #         if not model_provider:
    #             return None, Exception(f"ModelProvider with uuid {provider_uuid} not found")
    #
    #         for field, value in update_data.dict(exclude_unset=True).items():
    #             setattr(model_provider, field, value)
    #
    #         await self.db.commit()
    #         return model_provider, None
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         return None, e
    #
    # async def patch_model_provider(self, provider_uuid: str, patch_data: dict) -> Tuple[
    #     ModelProvider | None, Exception]:
    #     try:
    #         model_provider, error = await self.get_model_provider_by_uuid(provider_uuid)
    #         if error:
    #             return None, error
    #
    #         if not model_provider:
    #             return None, Exception(f"ModelProvider with uuid {provider_uuid} not found")
    #
    #         for field, value in patch_data.items():
    #             setattr(model_provider, field, value)
    #
    #         await self.db.commit()
    #         return model_provider, None
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         return None, e
    #
    # async def delete_model_provider(self, provider_uuid: str) -> Tuple[bool, Exception | None]:
    #     try:
    #         model_provider = await self.get_model_provider_by_uuid(provider_uuid)
    #         if not model_provider:
    #             return False, Exception(f"ModelProvider with uuid {provider_uuid} not found")
    #
    #         await self.db.delete(model_provider)
    #         await self.db.commit()
    #         return True, None
    #     except SQLAlchemyError as e:
    #         await self.db.rollback()
    #         return False, e
