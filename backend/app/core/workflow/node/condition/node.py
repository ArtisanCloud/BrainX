from app.core.workflow.node.base import BaseNode


class ConditionNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)


    def execute(self, state: GraphState):
        print(f"Condition workflow: {self.name}, {state.messages}")
        state.messages.append("~~~finish Condition node here ")
        return state
