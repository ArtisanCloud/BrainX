import asyncio
import json

import ollama
from sqlalchemy.ext.asyncio import AsyncSession
from app import settings
from fastapi import Request

from app.core.brainx.base import LLMModel
from app.logger import logger
from app.models.robot_chat.conversation import Conversation
from app.schemas.robot_chat.chat import RequestChat
from app.service.app.service import AppService
from app.service.brainx.service import BrainXService
from app.service.conversation.service import ConversationService
from app.utils.chat import generate_session_id
from app.utils.media import remove_base64_images_prefix


async def agent_chat_event_generator(
        request: Request, data: RequestChat, user_uuid: str, async_db: AsyncSession
):
    # 第一次响应发送“处理中”消息
    yield f"data: {json.dumps({'status': 'processing'})}\n\n"

    # 这里模拟等待几秒钟 `agent_chat` 的响应，不会打断前端的 SSE 连接
    try:
        question = data.messages[0].content
        app_uuid = data.appUUID
        conversation_uuid = data.conversationUUID
        base64_images = remove_base64_images_prefix(data.images)
        # print("conversationUUID:", conversation_uuid)
        # 等待 agent_chat 的实际响应（这可能耗时几秒）
        stream_response, conversation_uuid, exception = await agent_chat(
            async_db=async_db,
            question=question,
            images=base64_images,
            llm=data.llm,
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
            yield f"data: {json.dumps({'status': 'data', 'content': content})}\n\n"
            await asyncio.sleep(0.1)  # 控制消息发送频率

    except Exception as e:
        error_msg = "robot chat inner error"
        logger.error(
            f"Failed to generate event stream: {e}", exc_info=settings.log.exc_info
        )
        yield f"data: {json.dumps({'status': 'error', 'message': error_msg})}\n\n"
        await async_db.rollback()
    finally:
        yield f"data: {json.dumps({'status': 'finished'})}\n\n"
        await async_db.close()


async def agent_chat(
        async_db: AsyncSession,
        app_uuid: str,
        user_uuid: str,
        question: str,
        llm: str,
        conversation_uuid: str = "",
        images: list[str] | None = None,
):
    try:
        # 获取app
        service_app = AppService(async_db)
        app, exception = await service_app.app_dao.get_app_by_uuid_with_preloads(
            app_uuid
        )
        if exception:
            return None, None, exception
        # stream_response = chat_by_llm(question, llm, app, 0.5)
        service_brain_x = BrainXService(
            llm=llm,
            async_db=async_db,
            streaming=True,
            app=app,
        )

        # 如果不是app的对话，则生成临时的新会话ID
        if app_uuid == "" and conversation_uuid == "":
            conversation_uuid = generate_session_id()

        elif app_uuid != "" and conversation_uuid != "":
            # 如果是app的对话，则从数据库中获取对话历史记录
            service_conversation = ConversationService(async_db)
            conversation, exception = (
                await service_conversation.conversation_dao.async_get_by_uuid(
                    conversation_uuid
                )
            )
            if exception:
                return None, None, exception

            # 如果对话历史记录不存在，则创建新的对话历史记录
            question = question[:15] if len(question) > 15 else question
            if conversation is None:
                new_conversation, exception = (
                    await service_conversation.conversation_dao.async_create(
                        Conversation(
                            uuid=conversation_uuid,
                            user_uuid=user_uuid,
                            app_uuid=app_uuid,
                            name=question,
                        )
                    )
                )
                if exception:
                    return None, None, exception
            # 如果存在对话历史记录，则直接使用该对话历史记录
            else:
                # print(conversation)
                # print(conversation.user_uuid, user_uuid, conversation.app_uuid, app_uuid)
                # print(type(conversation.user_uuid), type(user_uuid))
                # print(type(conversation.app_uuid), type(app_uuid))

                if (
                        str(conversation.user_uuid) != user_uuid
                        or str(conversation.app_uuid) != app_uuid
                ):
                    return (
                        None,
                        None,
                        Exception(
                            "Conversation "
                            + conversation_uuid
                            + " not belong to this app or tenant"
                        ),
                    )

        if images is None or len(images) == 0:
            stream_response, exception = service_brain_x.agent_chat(
                question=question, session_id=conversation_uuid
            )
        else:
            stream_response = ollama.chat(
                model=LLMModel.OLLAMA_LLAMA3_2_VISION.value,
                stream=True,
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "images": images,
                    }
                ],
            )

        if exception:
            return None, None, exception

        return stream_response, conversation_uuid, None

    except Exception as e:
        return None, None, e
