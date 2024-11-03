from typing import Dict, Any, Tuple, Iterator

from app.core.rag.synthesis.drivers.langchain.executor import LangchainAgentExecutor
from app.models import App


class LanggraphAgentExecutor(LangchainAgentExecutor):
    def __init__(self,
                 llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 **kwargs):
        super().__init__(llm=llm, temperature=temperature, streaming=streaming, **kwargs)

    def chat_stream(self,
                    question: Dict,
                    app: App = None,
                    temperature: float = 0.5,
                    session_id: str = "",
                    **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        try:
            # 1. Get the conversation history from the database
            pass

        except Exception as e:
            return None, e