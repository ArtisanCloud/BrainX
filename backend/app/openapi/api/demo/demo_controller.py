import http
import asyncio

from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app import settings
from app.api.chat_bot.chat_controller import event_generator
from app.database.deps import get_async_db_session
from app.database.seed import init_user_uuid
from app.logger import logger
from app.openapi.schemas.demo import ResponseHelloWorld, RequestHelloWorld, RequestEchoLongTime, ResponseEchoLongTime
from app.schemas.question_answer.query import RequestQuery
from app.service.robot_chat.chat import chat

router = APIRouter()


@router.post("/hello-world")
async def api_hello_world(
        data: RequestHelloWorld,
) -> ResponseHelloWorld:
    res = ResponseHelloWorld(
        message=f"hi {data.name}, I get your message '{data.message}'"
    )

    return res


@router.post("/echo-long-time")
async def api_echo_long_time(
        data: RequestEchoLongTime,
) -> ResponseEchoLongTime:
    timeout = data.timeout
    logger.info(f"Received timeout value: {timeout}")

    if timeout > 60:
        timeout = 60
    elif timeout < 0:
        timeout = 3

    logger.info(f"Adjusted timeout value: {timeout}")

    async def long_running_task(timeout: int) -> ResponseEchoLongTime:
        try:
            logger.info(f"Starting long running task for {timeout} seconds")
            await asyncio.sleep(timeout)
            return ResponseEchoLongTime(
                message=f"thank you for waiting for '{timeout}' seconds"
            )
        except asyncio.CancelledError:
            logger.warning("Task was cancelled")
            # 不抛出异常，简单记录日志即可
            return ResponseEchoLongTime(message=f"Task was cancelled by '{timeout}'")

    try:
        # 创建一个异步任务来处理长时间操作
        res = await asyncio.wait_for(long_running_task(timeout), timeout=timeout)
        logger.info(f"Task completed successfully with message: {res.message}")
    except asyncio.TimeoutError:
        logger.error("Request timed out", exc_info=settings.log.exc_info)
        raise HTTPException(status_code=504, detail="Request timed out")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=settings.log.exc_info)
        raise HTTPException(status_code=500, detail=str(e))

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
