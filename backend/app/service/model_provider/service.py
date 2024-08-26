from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model_provider.provider_model import ProviderModel
from app.schemas.model_provider.model_provider import ProviderModelSchema
from app.dao.model_provider.provider import ProviderModelDAO


class ProviderModelService:
    def __init__(self, db: AsyncSession):
        self.model_provider_dao = ProviderModelDAO(db)

    async def create_model_provider(self, provider_data: ProviderModelSchema) -> Tuple[
        ProviderModel | None, Exception | None]:
        return await self.model_provider_dao.create_model_provider(provider_data)

    async def get_model_provider_by_uuid(self, provider_uuid: str) -> Tuple[ProviderModel | None, Exception | None]:
        return await self.model_provider_dao.get_model_provider_by_uuid(provider_uuid)

    async def update_model_provider(self, provider_uuid: str, update_data: ProviderModelSchema) -> Tuple[
        ProviderModel, Exception]:
        return await self.model_provider_dao.update_model_provider(provider_uuid, update_data)

    async def patch_model_provider(self, provider_uuid: str, patch_data: dict) -> Tuple[
        ProviderModel | None, Exception | None]:
        return await self.model_provider_dao.patch_model_provider(provider_uuid, patch_data)

    async def delete_model_provider(self, provider_uuid: str) -> Tuple[bool, Exception | None]:
        return await self.model_provider_dao.delete_model_provider(provider_uuid)
