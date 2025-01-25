import asyncio
import time
import json
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app import settings

from app.openapi.schemas.chat import (
    ChatResponseMessage,
    Choice,
    RequestOpenAIChat,
    ResponseOpenAIChat,
)
from app.service.robot_chat.agent_chat import agent_chat
from app.utils.media import remove_base64_images_prefix


async def agent_openai_chat_event_generator(
    request: Request, data: RequestOpenAIChat, user_uuid: str, db: AsyncSession
):
    # 第一次响应发送“处理中”消息
    yield f"data: {json.dumps({'status': 'processing'})}\n\n"

    # 这里模拟等待几秒钟 `agent_chat` 的响应，不会打断前端的 SSE 连接
    try:
        question = data.messages[0].content
        app_uuid = data.app_uuid
        conversation_uuid = data.conversation_uuid
        base64_images = remove_base64_images_prefix(data.images)
        # print("conversationUUID:", conversation_uuid)
        # 等待 agent_chat 的实际响应（这可能耗时几秒）
        stream_response, conversation_uuid, exception = await agent_chat(
            db=db,
            question=question,
            images=base64_images,
            llm=data.model,
            user_uuid=user_uuid,
            app_uuid=app_uuid,
            conversation_uuid=conversation_uuid,
        )

        if exception is not None:
            raise exception

        # 返回实际内容
        for token in stream_response:
            if await request.is_disconnected():
                break  # 前端断开连接，停止生成

            content = token if isinstance(token, str) else token.content
            content = content.replace("\r\n", "\\n").replace("\n", "\\n")

            timestamp = int(time.time() * 1000)
            res = ResponseOpenAIChat(
                id=conversation_uuid,
                object="chat.completion.chunk",
                created=timestamp,
                model=data.model,
                system_fingerprint="fp_44709d6fcb",
                choices=[
                    Choice(
                        index=0,
                        delta=ChatResponseMessage(role="assistant", content=content),
                        finish_reason="stop",
                    )
                ],
                usage=None,
            )
            # print(res.model_dump())
            # yield f"{json.dumps(res.model_dump())}\n\n"
            yield f"data: {json.dumps(res.model_dump())}\n\n"
            await asyncio.sleep(0.1)  # 控制消息发送频率

    except Exception as e:
        error_msg = "robot chat inner error"
        logger.error(
            f"Failed to generate event stream: {e}", exc_info=settings.log.exc_info
        )
        yield f"data: {json.dumps({'status': 'error', 'message': error_msg})}\n\n"
        await db.rollback()
    finally:
        yield f"data: {json.dumps({'status': 'finished'})}\n\n"
        await db.close()
