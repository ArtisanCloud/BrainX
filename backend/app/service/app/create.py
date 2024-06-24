from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.app import AppSchema
from app.service.app.service import AppService

from app.models.app import App


def transform_app_to_reply(app: App) -> [AppSchema | None]:
    if app is None:
        return None

    return AppSchema.from_orm(app)


async def create_app(
        db: AsyncSession,
        app: App,
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(db)
    app, exception = await service_app.create_app(app)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
