from fastapi import APIRouter

from app.schemas.base import ResponseSchema
from app.schemas.workflow.node import ResponseGetNodeList
from app.service.workflow.node.list import get_node_list

router = APIRouter()


@router.get("/list")
async def api_get_node_list() -> ResponseGetNodeList | ResponseSchema:
    nodes = await get_node_list()
    res = ResponseGetNodeList(data=nodes)

    return res
