
from typing import Annotated, Sequence, TypedDict, List

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel


# https://github.com/langchain-ai/langgraph/blob/main/examples/state-model.ipynb
# How to use Pydantic model as state
class GraphState(BaseModel):
    question: str = ""
    result: str = ""
    messages: Annotated[list, add_messages]