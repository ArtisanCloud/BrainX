import asyncio
import http
from typing import Iterator

from fastapi import Request, APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.middleware.auth import get_session_user
from app.core.brain.index import LLMModel
from app.database.deps import get_db_session
from app.database.seed.user import init_user_uuid
from app.logger import logger
from app.models import User
from app.schemas.robot_chat.chat import RequestChat
from app.service.robot_chat.chat import chat

router = APIRouter()


async def event_generator(request: Request, llm: str, stream_response: Iterator):
    for token in stream_response:
        # print("llm:", llm, "token:", token)
        if await request.is_disconnected():
            break

        if token:
            content = ''
            if llm == LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
                # print("token content:", repr(token.content), end='\n')
                if isinstance(token.content, str):
                    # print("turbo", repr(token.content), end='\n')
                    content = token.content

            elif llm == LLMModel.KIMI_MOONSHOT_V1_8K.value:
                if isinstance(token.content, str):
                    content = token.content

            elif llm in [
                LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value,
                LLMModel.BAIDU_ERNIE_3_D_5_8K.value,
                LLMModel.BAIDU_ERNIE_4_D_0_8K.value,
                LLMModel.BAIDU_ERNIE_Speed_128K.value,
                LLMModel.BAIDU_ERNIE_Lite_8K.value
            ]:
                if isinstance(token.content, str):
                    # 替换回车为转义的 `\n`
                    # print(repr(token.content))
                    content = token.content.replace("\r\n", "\\n").replace("\n", "\\n")

            else:
                # print("token content:", repr(token), end='\n')
                if token != "":
                    content = token

            # print("content end:", content, end='\n\n')
            # if content:
            yield f"data: {content}\n\n"
            await asyncio.sleep(0.1)  # 延迟一点时间


@router.post("/chat")
async def api_chat(
        request: Request,
        data: RequestChat,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    try:
        question = data.messages[0].content
        # user_uuid = data.appUUID
        app_uuid = data.appUUID
        conversation_uuid = data.conversationUUID

        stream_response, conversation_uuid, exception = await chat(
            db,
            question, data.llm,
            session_user.uuid, app_uuid, conversation_uuid
        )
        if exception:
            logger.error(exception)
            raise Exception("database query: pls check log")

        # print("conversationUUID:", conversation_uuid)
        return StreamingResponse(
            event_generator(request, data.llm, stream_response),
            media_type="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Conversation-Uuid": conversation_uuid
            },
        )

    except Exception as e:
        # logger.error(f"Failed to robot_chat: {e}")
        return StreamingResponse(
            [f"data: ERROR: {e}\n\n"],
            media_type="text/event-stream",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
