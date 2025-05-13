from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class LLMNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        super().execute(state)

        
        return {"messages": ""}
