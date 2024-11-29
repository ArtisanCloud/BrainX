import http

from fastapi import Request, APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.api.middleware.auth import get_session_user
from app.database.deps import get_async_db_session
from app.logger import logger
from app.models import User
from app.openapi.schemas.chat import RequestOpenAIChat
from app.openapi.service.robot_chat.openai import agent_openai_chat_event_generator
from app.schemas.robot_chat.chat import RequestChat
from app.service.robot_chat.agent_chat import agent_chat_event_generator
from app.service.robot_chat.chat import chat_event_generator

from app.database.seed.user import init_user_uuid

router = APIRouter()


@router.post("/chat")
async def api_chat(
        request: Request,
        data: RequestChat,
        # session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_async_db_session),
) -> StreamingResponse:
    try:
        session_user = User(uuid=init_user_uuid)
        # print("conversationUUID:", data)
        return StreamingResponse(
            chat_event_generator(
                request=request, data=data,
                user_uuid=str(session_user.uuid), db=db
            ),
            media_type="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Conversation-Uuid": data.conversationUUID
            },
        )

    except Exception as e:
        logger.error(f"Failed to robot_chat: {e}", exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return StreamingResponse(
            [f"data: ERROR: {e}\n\n"],
            media_type="text/event-stream",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )


@router.post("/agent/chat")
async def api_agent_chat(
        request: Request,
        data: RequestChat,
        # session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_async_db_session),
) -> StreamingResponse:
    try:
        session_user = User(uuid=init_user_uuid)
        return StreamingResponse(
            agent_chat_event_generator(
                request=request, data=data,
                user_uuid=str(session_user.uuid), db=db
            ),
            media_type="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Conversation-Uuid": data.conversationUUID
            },
        )

    except Exception as e:
        logger.error(f"Failed to agent robot_chat: {e}", exc_info=settings.log.exc_info)
        return StreamingResponse(
            [f"data: ERROR: system inner error. \n\n"],
            media_type="text/event-stream",
            status_code=http.HTTPStatus.BAD_REQUEST,
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                # "Conversation-Uuid": conversation_uuid
            },
        )


@router.post("/agent/openai/chat")
async def api_agent_chat(
        request: Request,
        data: RequestOpenAIChat,
        # session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_async_db_session),
) -> StreamingResponse:
    try:
        session_user = User(uuid=init_user_uuid)
        return StreamingResponse(
            agent_openai_chat_event_generator(
                request=request, data=data,
                user_uuid=str(session_user.uuid), db=db
            ),
            media_type="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Conversation-Uuid": data.conversation_uuid
            },
        )

    except Exception as e:
        logger.error(f"Failed to agent robot_chat: {e}", exc_info=settings.log.exc_info)
        return StreamingResponse(
            [f"data: ERROR: system inner error. \n\n"],
            media_type="text/event-stream",
            status_code=http.HTTPStatus.BAD_REQUEST,
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                # "Conversation-Uuid": conversation_uuid
            },
        )