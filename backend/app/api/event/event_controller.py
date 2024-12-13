from fastapi import APIRouter

from app import settings
from app.events.manager import event_manager
from app.schemas.event.schema import RequestPublishEvent

router = APIRouter()


@router.post("/publish_event/")
async def publish_event(event_data: RequestPublishEvent):
    data_dict = dict(event_data.__dict__)
    await event_manager.publish_event(settings.event.default_event_queue, data_dict)
    return {"message": "Event published successfully"}
