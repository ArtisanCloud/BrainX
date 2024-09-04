from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class VariableNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        print(f"Variable workflow: {self.name}, {state.messages}")
        state.messages.append("~~~finish Variable node here ")
        return state
