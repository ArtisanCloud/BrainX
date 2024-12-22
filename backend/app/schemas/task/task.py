from typing import List

from pydantic import conint

from app.schemas.base import BaseSchema


class RequestRunMultiple30SecondsStatus(BaseSchema):
    task_count: conint(ge=1, le=6) = 2

class RequestQueryDocumentProcessStatus(BaseSchema):
    task_uuids: List[str]