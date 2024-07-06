from typing import Callable, Dict, Any

class Node:
    def __init__(self, id: str, name: str, task: Callable, next_node: 'Node' = None):
        self.id = id
        self.name = name
        self.task = task
        self.next_node = next_node

    def execute(self, *args, **kwargs):
        print(f"Executing node: {self.name}")
        return self.task(*args, **kwargs)

class Workflow:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.start_node: Node = None

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        if not self.start_node:
            self.start_node = node

    def set_next_node(self, current_node_id: str, next_node_id: str):
        if current_node_id in self.nodes and next_node_id in self.nodes:
            self.nodes[current_node_id].next_node = self.nodes[next_node_id]

    def execute(self, *args, **kwargs):
        current_node = self.start_node
        while current_node:
            result = current_node.execute(*args, **kwargs)
            current_node = current_node.next_node
        print("Workflow completed.")