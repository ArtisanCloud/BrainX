import http
import uuid

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.database.base import PER_PAGE, PAGE
from app.database.deps import get_db_session
from app.database.seed.user import init_user_uuid
from app.logger import logger
from app.models.robot_chat.conversation import Conversation
from app.schemas.base import ResponseSchema, Pagination
from app.schemas.robot_chat.conversation import RequestCreateConversation, make_conversation, \
    ResponseCreateConversation, RequestPatchConversation, ResponsePatchConversation, ResponseDeleteConversation, \
    ResponseGetConversationList
from app.service.conversation.delete import soft_delete_conversation
from app.service.conversation.list import get_conversation_list
from app.service.conversation.create import create_conversation
from app.service.conversation.patch import patch_conversation

router = APIRouter()


@router.get("/list")
async def api_get_conversation_list(
        request: Request,
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetConversationList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", PAGE))
    page_size = int(request.query_params.get("page_size", PER_PAGE))
    app_uuid = request.query_params.get("app_uuid", None)
    p = Pagination(page=page, page_size=page_size)
    # print("app_uuid:", app_uuid)

    try:
        conversations, pagination, exception = await get_conversation_list(db, p, app_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetConversationList(data=conversations, pagination=pagination)

    return res


@router.get("/{conversation_id}")
async def api_get_conversation_by_id(conversation_id: int, db: AsyncSession = Depends(get_db_session)):
    conversation = await db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/create")
async def api_create_conversation(
        data: RequestCreateConversation,
        db: AsyncSession = Depends(get_db_session)):
    try:

        conversation = make_conversation(data)
        conversation.user_uuid = uuid.UUID(init_user_uuid)

        conversation, exception = await create_conversation(db, conversation)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseCreateConversation(conversation=conversation)

    return res


@router.patch("/patch/{conversation_uuid}")
async def api_patch_conversation(
        conversation_uuid: str,  # 接收路径参数 conversation_uuid
        data: RequestPatchConversation,
        db: AsyncSession = Depends(get_db_session)):
    try:

        update_data = data.dict(exclude_unset=True)
        # print(conversation_uuid, update_data)

        conversation, exception = await patch_conversation(db, conversation_uuid, update_data)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponsePatchConversation(conversation=conversation)

    return res


@router.delete("/delete/{conversation_uuid}")
async def api_delete_conversation(
        conversation_uuid: str,  # 接收路径参数 conversation_uuid
        db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = 1
        result, exception = await soft_delete_conversation(db, user_id, conversation_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseDeleteConversation(result=result)

    return res
