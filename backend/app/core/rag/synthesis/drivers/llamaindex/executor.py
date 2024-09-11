from typing import Optional, Any, List

from app.core.rag.synthesis.interface import BaseAgentExecutor


class LlamaIndexAgentExecutor(BaseAgentExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def invoke(self, query: str, config: Optional[Any] = None, **kwargs: Any) -> str:
        return ""

    def stream(self, query: str, config: Optional[Any] = None, **kwargs: Any) -> Any:
        return

    def completion(self, query: str, config: Optional[Any] = None, **kwargs: Any) -> str:
        return ""

    def execute(self, tasks: List[str], config: Optional[Any] = None, **kwargs: Any) -> List[str]:
        return []
