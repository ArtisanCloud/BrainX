from dataclasses import  field
from typing import List, Any

from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState

class PluginNode(BaseNode):
    tools: List[Any] = field(default_factory=list)

    def __init__(self, node_data: dict):
        super().__init__(node_data)
        self.tools = node_data.get("tools", [])

    def execute(self, state: GraphState):
        super().execute(state)

        state.messages.append("~~~finish plugin node here ")
        return state
