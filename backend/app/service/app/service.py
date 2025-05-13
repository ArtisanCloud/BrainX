from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.app.app import AppDAO
from app.models import App
from app.models.app.app_model_config import AppModelConfig
from app.models.rag.dataset import Dataset
from app.schemas.app.app import AppSchema
from app.schemas.app.app_model_config import AppModelConfigSchema
from app.schemas.rag.dataset import DatasetSchema
from app.service.rag.dataset.service import transform_dataset_to_reply


class AppService:
    def __init__(self,async_db: AsyncSession):
        self.app_dao = AppDAO(async_db)


def transform_app_model_config_to_reply(
    app_model_config: AppModelConfig,
) -> [AppModelConfigSchema | None]:
    if app_model_config is None:
        return None
    return AppModelConfigSchema.from_orm(app_model_config)


def transform_connect_dataset_to_reply(dataset: Dataset) -> [str | None]:
    if dataset is None:
        return None

    dataset_schema = DatasetSchema.from_orm(dataset)
    return dataset_schema


def transform_connect_datasets_to_reply(datasets: [Dataset]) -> [List[str] | None]:
    data = [transform_dataset_to_reply(dataset) for dataset in datasets]
    # print(data)
    return data


def transform_app_to_reply(app: App) -> [AppSchema | None]:
    if app is None:
        return None

    app_schema = AppSchema.from_orm(app)

    if app.connected_datasets:
        app_schema.connected_datasets = transform_connect_datasets_to_reply(
            app.connected_datasets
        )

    if app.current_app_model_config:
        app_schema.current_app_model_config = transform_app_model_config_to_reply(
            app.current_app_model_config
        )

    return app_schema


def transform_apps_to_reply(apps: [App]) -> List[AppSchema]:
    data = [transform_app_to_reply(app) for app in apps]
    # print(data)
    return data
