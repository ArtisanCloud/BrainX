from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import App, User
from app.service.app.create import transform_app_to_reply
from app.service.app.service import AppService


async def get_app_by_uuid(
       async_db: AsyncSession,
        user: User,
        app_uuid: str
) -> Tuple[App | None, Exception | None]:
    service_app = AppService(async_db)
    app, exception = await service_app.app_dao.get_app_by_uuid_with_preloads(app_uuid)

    if exception:
        return None, exception
    if app is None:
        return None, Exception("object not found")

    # check if the app is belong to the user's tenant
    if app.tenant_uuid != user.tenant_owner_uuid:
        return None, Exception("Object is not belong to your owned tenant")

    return transform_app_to_reply(app), None
