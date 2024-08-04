from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MediaResource, User
from app.service.media_resource.create import transform_media_resource_to_reply
from app.service.media_resource.service import MediaResourceService


async def get_media_resource_by_uuid(
        db: AsyncSession,
        user: User,
        media_resource_uuid: str
) -> Tuple[MediaResource | None, Exception | None]:
    service_media_resource = MediaResourceService(db)
    media_resource, exception = await (
        service_media_resource.
        media_resource_dao.
        get_by_uuid(media_resource_uuid)
    )

    if exception:
        return None, exception
    if media_resource is None:
        return None, Exception("object not found")

    # check if the media_resource is belong to the user's tenant
    if media_resource.tenant_uuid != user.tenant_owner_uuid:
        return None, Exception("Object is not belong to your owned tenant")

    return transform_media_resource_to_reply(media_resource), None
