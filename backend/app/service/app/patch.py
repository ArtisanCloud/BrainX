from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.app.app import AppSchema
from app.service.app.create import transform_app_to_reply
from app.service.app.service import AppService


async def patch_app(
        db: AsyncSession,
        app_uuid: str,
        update_data: Dict[str, Any]
) -> Tuple[AppSchema | None, Exception | None]:
    service_app = AppService(db)
    app, exception = await service_app.app_dao.patch(app_uuid, update_data)

    if exception:
        return None, exception

    return transform_app_to_reply(app), None
