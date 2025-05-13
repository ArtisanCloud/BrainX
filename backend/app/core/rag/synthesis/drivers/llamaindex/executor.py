from typing import Optional, Any, List, Dict, Iterator, Tuple

from app.core.rag.synthesis.interface import BaseAgentExecutor
from app.models import App


class LlamaIndexAgentExecutor(BaseAgentExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def stream(self, query: Any,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:
        return None, None

    def invoke(self, query: Any,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               output_schemas: Any = None,
               **kwargs: Any) -> Tuple[Any | None, Exception | None]:
        return None, None

    def chat_completion(self,
                        question: Any,
                        temperature: float = 0.5,
                        app: App = None,
                        session_id: str = "",
                        **kwargs: Any) -> Tuple[str, Exception | None]:
        return "", None

    def chat_stream(self,
                    question: Any,
                    temperature: float = 0.5,
                    app: App = None,
                    session_id: str = "",
                    **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:
        return None, None
