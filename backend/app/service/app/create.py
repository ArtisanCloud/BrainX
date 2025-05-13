from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.app.app import AppSchema
from app.service.app.service import AppService, transform_app_to_reply

from app.models.app.app import App


async def create_app(
        async_db: AsyncSession,
        app: App,
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(async_db)
    app, exception = await service_app.app_dao.async_create(app)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
