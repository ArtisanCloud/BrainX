from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.app.app import AppSchema
from app.service.app.service import AppService

from app.models.app.app import App


def transform_app_to_reply(app: App) -> [AppSchema | None]:
    if app is None:
        return None

    return AppSchema.from_orm(app)


async def create_app(
        db: AsyncSession,
        app: App,
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(db)
    app, exception = await service_app.app_dao.async_create(app)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
