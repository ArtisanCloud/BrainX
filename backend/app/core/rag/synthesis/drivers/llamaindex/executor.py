from typing import Optional, Any, List, Dict

from app.core.rag.synthesis.interface import BaseAgentExecutor


class LlamaIndexAgentExecutor(BaseAgentExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def invoke(self, query: Dict, config: Optional[Any] = None, **kwargs: Any) -> str:
        return ""

    def stream(self, query: Dict, config: Optional[Any] = None, **kwargs: Any) -> Any:
        return

    def completion(self, query: Dict, config: Optional[Any] = None, **kwargs: Any) -> str:
        return ""

    def execute(self, tasks: List[str], config: Optional[Any] = None, **kwargs: Any) -> List[str]:
        return []
