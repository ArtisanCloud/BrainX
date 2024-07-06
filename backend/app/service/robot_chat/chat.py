from app import settings
from app.models.app import App
from app.service.brainx import BrainXService


def chat(question: str, llm: str, role: str = None, conversation_uuid: str = ''):
    app = App(name=role)
    app.persona_prompt = "You are a helpful assistant. Answer all questions to the best of your ability."

    # stream_response = chat_by_llm(question, llm, app, 0.5)
    service_brain_x = BrainXService(
        llm, 0.5, True,
        chat_history_kwargs={
            "url": settings.cache.redis.url,
        })

    if conversation_uuid == '':
        conversation_uuid = service_brain_x.generate_session_id()

    stream_response, exception = service_brain_x.chat_stream(question, app, conversation_uuid)
    if exception:
        return None, exception

    return stream_response, conversation_uuid, None
