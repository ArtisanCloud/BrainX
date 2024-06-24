from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.app.service import AppService


async def soft_delete_app(
        db: AsyncSession,
        user_id: int,
        app_uuid: str
) -> Tuple[bool | None, Exception | None]:
    service_app = AppService(db)
    result, exception = await service_app.soft_delete_app(user_id, app_uuid)

    if exception:
        return False, exception

    return result, None
