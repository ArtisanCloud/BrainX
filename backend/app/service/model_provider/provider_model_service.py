from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.model_provider.provider_model import ProviderModelDAO
from app.models.model_provider.provider_model import ProviderModel
from app.schemas.model_provider.provider import ProviderModelSchema


class ProviderModelService:
    def __init__(self, db: AsyncSession):
        self.model_provider_dao = ProviderModelDAO(db)
