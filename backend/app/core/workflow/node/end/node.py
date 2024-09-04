from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class EndNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        super().execute(state)

        # node_list = self.context_manager.get_node_list()
        print(f"---"
              # f"dataset: {self.datasets}, "
              # f"node_list: {node_list}"
              f"inputs: {self.input_vars}"
              f"---")

        state.messages.append("~~~finish end node here ")
        return state
