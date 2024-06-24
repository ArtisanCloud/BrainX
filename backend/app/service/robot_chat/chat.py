from app.models.app import App
from app.service.brainx import BrainXService


def chat(question: str, llm: str, role: str = None):
    app = App(name=role)
    app.persona_prompt = "You are a helpful assistant. Answer all questions to the best of your ability."

    # stream_response = chat_by_llm(question, llm, app, 0.5)
    service_brain_x = BrainXService(llm, 0.5, True)
    stream_response, exception = service_brain_x.chat_stream(question, app, "test_session_id")
    if exception:
        return None, exception

    return stream_response, None
