from typing import List, Any

from app.core.workflow.node.base import NodeInfo
from app.schemas.base import BaseSchema


class ResponseGetNodeInfoList(BaseSchema):
    data: List[NodeInfo]

