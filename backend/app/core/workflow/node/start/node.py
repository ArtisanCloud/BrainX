from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class StartNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        super().execute(state)

        state.messages.append("~~~finish start node here ")
        return state
