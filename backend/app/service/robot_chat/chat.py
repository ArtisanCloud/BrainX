from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.models.app import App
from app.models.robot_chat.conversation import Conversation
from app.service.app.service import AppService
from app.service.brainx import BrainXService
from app.service.conversation.service import ConversationService


async def chat(db: AsyncSession,
               question: str, llm: str,
               user_uuid: str = None, app_uuid: str = None, conversation_uuid: str = ''
               ):
    if app_uuid != '':
        # 获取app
        service_app = AppService(db)
        app, exception = await service_app.get_app_by_uuid(app_uuid)
        if exception:
            return None, None, exception
    else:
        app = App()

    # stream_response = chat_by_llm(question, llm, app, 0.5)
    service_brain_x = BrainXService(
        llm, 0.5, True,
        chat_history_kwargs={
            "url": settings.cache.redis.url,
        })

    # 如果不是app的对话，则生成临时的新会话ID
    if app_uuid == '' and conversation_uuid == '':
        conversation_uuid = service_brain_x.generate_session_id()

    elif app_uuid != '' and conversation_uuid != '':
        # 如果是app的对话，则从数据库中获取对话历史记录
        service_conversation = ConversationService(db)
        conversation, exception = await service_conversation.conversation_dao.get_by_uuid(conversation_uuid)
        if exception:
            return None, None, exception

        # 如果对话历史记录不存在，则创建新的对话历史记录
        question = question[:15] if len(question) > 15 else question
        if conversation is None:
            new_conversation, exception = await service_conversation.conversation_dao.create(Conversation(
                uuid=conversation_uuid,
                user_uuid=user_uuid,
                app_uuid=app_uuid,
                name=question,
            ))
            if exception:
                return None, None, exception
        # 如果存在对话历史记录，则直接使用该对话历史记录
        else:
            if conversation.user_uuid != user_uuid or conversation.app_uuid != app_uuid:
                return None, None, Exception("Conversation " + conversation_uuid + " not belong to this app or user")

    stream_response, exception = service_brain_x.chat_stream(question, app, conversation_uuid)
    if exception:
        return None, exception

    return stream_response, conversation_uuid, None
