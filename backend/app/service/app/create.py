from typing import Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.logger import logger
from app.models import Dataset, AppModelConfig
from app.schemas.app.app import AppSchema
from app.schemas.app.app_model_config import AppModelConfigSchema
from app.service.app.service import AppService

from app.models.app.app import App


def transform_app_model_config_to_reply(app_model_config: AppModelConfig) -> [AppModelConfigSchema | None]:
    if app_model_config is None:
        return None
    return AppModelConfigSchema.from_orm(app_model_config)


def transform_connect_datasets_to_reply(datasets: [Dataset]) -> [List[str] | None]:
    data = [dataset.uuid for dataset in datasets]
    # print(data)
    return data


def transform_app_to_reply(app: App) -> [AppSchema | None]:
    if app is None:
        return None

    app_schema = AppSchema.from_orm(app)

    # if app.connected_datasets:
    #     appSchema.connected_datasets = transform_connect_datasets_to_reply(app.connected_datasets)
    try:
        app_model_config = app.current_app_model_config
        if isinstance(app_model_config, AppModelConfig):
            app_schema.current_app_model_config = transform_app_model_config_to_reply(app_model_config)
    except Exception as e:
        logger.warn(e, exc_info=settings.log.exc_info)

    return app_schema


async def create_app(
        db: AsyncSession,
        app: App,
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(db)
    app, exception = await service_app.app_dao.async_create(app)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
