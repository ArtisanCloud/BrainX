from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core.brainx.chat.app import generate_session_id
from app.models.app.app import App
from app.models.robot_chat.conversation import Conversation
from app.service.app.service import AppService
from app.service.brainx.service import BrainXService
from app.service.conversation.service import ConversationService


async def chat(db: AsyncSession,
               question: str, llm: str,
               user_uuid: str = None, app_uuid: str = None, conversation_uuid: str = ''
               ):
    if app_uuid != '':
        # 获取app
        service_app = AppService(db)
        app, exception = await service_app.app_dao.async_get_by_uuid(app_uuid)

        if exception:
            return None, None, exception
    else:
        app = App()

    # stream_response = chat_by_llm(question, llm, app, 0.5)
    service_brain_x = BrainXService(
        llm,
        streaming=True,
        table_name=settings.database.table_name_vector_store,
    )

    # print(
    #     "question:", question, "llm:", llm,
    #     "user_uuid:", user_uuid,
    #     "app_uuid:", app_uuid, "conversation_uuid:", conversation_uuid
    # )

    # 如果不是app的对话，则生成临时的新会话ID
    if app_uuid == '' and conversation_uuid == '':
        conversation_uuid = generate_session_id()

    elif app_uuid != '' and conversation_uuid != '':
        # 如果是app的对话，则从数据库中获取对话历史记录
        service_conversation = ConversationService(db)
        conversation, exception = await service_conversation.conversation_dao.async_get_by_uuid(conversation_uuid)
        if exception:
            return None, None, exception

        # 如果对话历史记录不存在，则创建新的对话历史记录
        question = question[:15] if len(question) > 15 else question
        if conversation is None:
            new_conversation, exception = await service_conversation.conversation_dao.async_create(Conversation(
                uuid=conversation_uuid,
                user_uuid=user_uuid,
                app_uuid=app_uuid,
                name=question,
            ))
            if exception:
                return None, None, exception
        # 如果存在对话历史记录，则直接使用该对话历史记录
        else:
            # print(conversation)
            # print(conversation.user_uuid, user_uuid, conversation.app_uuid, app_uuid)
            # print(type(conversation.user_uuid), type(user_uuid))
            # print(type(conversation.app_uuid), type(app_uuid))

            if str(conversation.user_uuid) != user_uuid or str(conversation.app_uuid) != app_uuid:
                return None, None, Exception("Conversation " + conversation_uuid + " not belong to this app or tenant")

    stream_response, exception = service_brain_x.chat_stream(
        question={"question": question}, temperature=0.5,
        app=app, session_id=conversation_uuid
    )
    if exception:
        return None, None, exception

    return stream_response, conversation_uuid, None
