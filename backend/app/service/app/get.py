from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app.app import App


async def get_app_by_id(
        db: AsyncSession,
        app_id: int
) -> App:
    return await db.get(App, app_id)

