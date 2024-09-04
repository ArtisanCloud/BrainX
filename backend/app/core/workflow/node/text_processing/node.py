from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class TextProcessingNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        print(f"Text Processing workflow: {self.name}, {state.messages}")
        state.messages.append("~~~finish TextProcessing node here ")
        return state
