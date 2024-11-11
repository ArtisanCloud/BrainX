import asyncio
import json
from typing import Iterator

import ollama
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core.brainx.base import LLMModel
from app.core.brainx.chat.app import generate_session_id
from app.logger import logger
from app.models.app.app import App
from app.models.robot_chat.conversation import Conversation
from app.schemas.robot_chat.chat import RequestChat
from app.service.brainx.service import BrainXService
from app.service.conversation.service import ConversationService
from fastapi import Request

from app.utils.media import remove_base64_images_prefix


async def event_api_generator(request: Request, llm: str, stream_response: Iterator):
    try:
        for token in stream_response:
            # print("llm:", llm, "token:", token)
            if await request.is_disconnected():
                break

            if token:
                content = ""
                if llm in [
                    LLMModel.OPENAI_GPT_3_D_5_TURBO.value,
                    LLMModel.KIMI_MOONSHOT_V1_8K.value,
                ]:
                    # print("token content:", repr(token.content), end='\n')
                    if isinstance(token, str):
                        content = token
                    elif isinstance(token.content, str):
                        # print("turbo", repr(token.content), end='\n')
                        content = token.content

                elif llm in [
                    LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value,
                    LLMModel.BAIDU_ERNIE_3_D_5_8K.value,
                    LLMModel.BAIDU_ERNIE_4_D_0_8K.value,
                    LLMModel.BAIDU_ERNIE_Speed_128K.value,
                    LLMModel.BAIDU_ERNIE_Lite_8K.value,
                    LLMModel.OLLAMA_GEMMA_2B.value,
                    LLMModel.OLLAMA_GEMMA_7B.value,
                    LLMModel.OLLAMA_13B_ALPACA_16K.value,
                    LLMModel.OLLAMA_LLAMA3_2.value,
                ]:
                    if isinstance(token, str):
                        content = token
                    elif isinstance(token.content, str):
                        # 替换回车为转义的 `\n`
                        # print(repr(token.content))
                        content = token.content.replace("\r\n", "\\n").replace(
                            "\n", "\\n"
                        )

                else:
                    # print("token content:", repr(token), end='\n')
                    if token != "":
                        content = token

                # print("content end:", content, end='\n\n')
                # if content:
                yield f"data: {content}\n\n"
                await asyncio.sleep(0.1)  # 延迟一点时间
                # await asyncio.sleep(2)  # 延迟一点时间
    except Exception as e:
        logger.error(
            f"Failed to generate event stream: {e}", exc_info=settings.log.exc_info
        )
        return


async def chat_event_generator(
    request: Request, data: RequestChat, user_uuid: str, db: AsyncSession
):
    # 第一次响应发送“处理中”消息
    yield f"data: {json.dumps({'status': 'processing'})}\n\n"

    try:
        question = data.messages[0].content
        conversation_uuid = data.conversationUUID
        base64_images = remove_base64_images_prefix(data.images) 

        # 等待 agent_chat 的实际响应（这可能耗时几秒）
        stream_response, conversation_uuid, exception = await chat(
            db=db,
            question=question,
            images=base64_images,
            llm=data.llm,
            user_uuid=user_uuid,
            conversation_uuid=conversation_uuid,
        )

        if exception is not None:
            raise exception

        # 返回实际内容
        for token in stream_response:
            if await request.is_disconnected():
                break  # 前端断开连接，停止生成

            content = ''
            if isinstance(token, str):
                content = token
            elif hasattr(token, 'content'):
                content = token.content
            elif isinstance(token, dict):
                content = token.get('message', {}).get('content', '')
            
            if content:  # Only process if we have content
                content = content.replace("\r\n", "\\n").replace("\n", "\\n")
                yield f"data: {json.dumps({'status': 'data', 'content': content})}\n\n"
                await asyncio.sleep(0.1) 

    except Exception as e:
        error_msg = "inner error"
        logger.error(
            f"Failed to generate event stream: {e}", exc_info=settings.log.exc_info
        )
        yield f"data: {json.dumps({'status': 'error', 'message': error_msg})}\n\n"
        await db.rollback()
    finally:
        yield f"data: {json.dumps({'status': 'finished'})}\n\n"
        await db.close()


async def chat(
    db: AsyncSession,
    question: str,
    llm: str,
    images: list[str] | None = None,
    user_uuid: str = None,
    conversation_uuid: str = "",
):
    # print(question, images)
    # return None, None, None

    app = App()

    # stream_response = chat_by_llm(question, llm, app, 0.5)
    service_brain_x = BrainXService(
        llm,
        streaming=True,
    )

    # 如果不是app的对话，则生成临时的新会话ID
    if conversation_uuid == "":
        conversation_uuid = generate_session_id()

    elif conversation_uuid != "":
        # 如果是app的对话，则从数据库中获取对话历史记录
        service_conversation = ConversationService(db)
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

            if str(conversation.user_uuid) != user_uuid:
                return (
                    None,
                    None,
                    Exception(
                        "Conversation " + conversation_uuid + " not belong to tenant"
                    ),
                )

    if images is None or len(images) == 0:
        stream_response, exception = service_brain_x.chat_stream(
            question={"question": question},
            temperature=0.5,
            app=app,
            session_id=conversation_uuid,
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
