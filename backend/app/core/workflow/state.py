
from typing import Annotated, Sequence, TypedDict, List

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict


# https://github.com/langchain-ai/langgraph/blob/main/examples/state-model.ipynb
# How to use Pydantic model as state
class GraphState(TypedDict):
    question: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
