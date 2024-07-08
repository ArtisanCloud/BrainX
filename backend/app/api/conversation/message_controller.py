import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.api.context_manager import build_request_context
from app.database.deps import get_db_session
from app.schemas.base import ResponseSchema, Pagination
from app.schemas.robot_chat.conversation import ResponseGetMessageList
from app.service.message.list import get_cached_message_list

router = APIRouter()


@router.get("/list/cached")
async def api_get_message_list(
        request: Request,
        _=Depends(build_request_context),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetMessageList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))
    conversation_uuid = request.query_params.get("conversation_uuid", None)
    p = Pagination(page=page, page_size=page_size)
    # print("app_uuid:", app_uuid)

    try:
        messages, pagination, exception = await get_cached_message_list(db, conversation_uuid, p)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetMessageList(data=messages, pagination=pagination)

    return res
