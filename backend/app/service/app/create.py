from typing import Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.logger import logger
from app.models import Dataset, AppModelConfig
from app.schemas.app.app import AppSchema
from app.schemas.app.app_model_config import AppModelConfigSchema
from app.schemas.rag.dataset import DatasetSchema
from app.service.app.service import AppService, transform_app_to_reply

from app.models.app.app import App
from app.service.rag.dataset.create import transform_dataset_to_reply


async def create_app(
    db: AsyncSession,
    app: App,
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(db)
    app, exception = await service_app.app_dao.async_create(app)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
