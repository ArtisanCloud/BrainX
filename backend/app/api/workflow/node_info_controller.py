from fastapi import APIRouter

from app.schemas.base import ResponseSchema
from app.schemas.workflow.node import ResponseGetNodeInfoList
from app.service.workflow.node.list import get_node_info_list

router = APIRouter()


@router.get("/list")
async def api_get_node_info_list() -> ResponseGetNodeInfoList | ResponseSchema:
    nodes = await get_node_info_list()
    res = ResponseGetNodeInfoList(data=nodes)

    return res
