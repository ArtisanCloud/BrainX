import random

from starlette.requests import Request

from fastapi import APIRouter, Depends

from app.api.context_manager import build_request_context
from app.schemas.base import ResponseSchema
from app.schemas.open_doc.schema import ResponseGenerateDoc

router = APIRouter()


@router.post("/generate")
async def api_get_app_list(
        request: Request,
        _=Depends(build_request_context),
) -> ResponseGenerateDoc | ResponseSchema:
    docs = [
        "001",
        "002",
        "003",
    ]

    # 使用 random.choice() 从列表中随机选择一个元素
    selected_doc = random.choice(docs)

    return ResponseGenerateDoc(name=selected_doc)
