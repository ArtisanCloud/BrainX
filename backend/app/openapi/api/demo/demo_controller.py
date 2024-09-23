import http

from fastapi import Request, APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.api.chat_bot.chat_controller import event_generator
from app.database.deps import get_async_db_session
from app.database.seed import init_user_uuid
from app.logger import logger
from app.openapi.schemas.demo import ResponseHelloWorld, RequestHelloWorld
from app.schemas.question_answer.query import RequestQuery
from app.service.robot_chat.chat import chat

router = APIRouter()


@router.post("/hello-world")
async def api_hello_world(
        data: RequestHelloWorld,
) -> ResponseHelloWorld:
    res = ResponseHelloWorld(
        message=f"hi {data.name}, I get your messge '{data.message}'"
    )

    return res


@router.post("/stream")
async def api_chat(
        request: Request,
        data: RequestQuery,
        db: AsyncSession = Depends(get_async_db_session),
) -> StreamingResponse:
    try:
        question = data.question
        app_uuid = ""
        conversation_uuid = ""

        stream_response, conversation_uuid, exception = await chat(
            db,
            question, data.llm,
            init_user_uuid, app_uuid, conversation_uuid
        )
        if exception is not None:
            logger.error(exception)
            if isinstance(exception, SQLAlchemyError):
                raise Exception("database query: pls check log")
            raise exception

        return StreamingResponse(
            event_generator(request, data.llm, stream_response),
            media_type="text/event-stream",
            headers={"Content-Type": "text/event-stream"},
        )

    except Exception as e:
        return StreamingResponse(
            [f"data: ERROR: {e}\n\n"],
            media_type="text/event-stream",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
