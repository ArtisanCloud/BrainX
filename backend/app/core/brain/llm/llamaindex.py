from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

from app.core.config import settings


def get_openai_llm(llm: str, temperature: float, streaming: bool):
    return OpenAI(
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )

def get_ollama_llm(llm: str, temperature: float, streaming: bool):
    # print(settings.ollama.url)
    return Ollama(
        model=llm,
        base_url=settings.ollama.url,
        keep_alive=-1,
        temperature=temperature,
    )
