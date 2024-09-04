from typing import Any


class ContextManager:
    def __init__(self):
        self.ctx_key_node_list: str = "node_list"
        self.context = {}

    def set(self, key: str, value: Any):
        self.context[key] = value

    def get(self, key: str) -> Any:
        return self.context.get(key)

    def remove(self, key: str):
        if key in self.context:
            del self.context[key]

    def clear(self):
        self.context.clear()

    def get_node_list(self):
        # print("to get node list:", self.context)
        node_list = self.context.get(self.ctx_key_node_list, {})
        return node_list

    def get_node(self, node_id):
        node_list = self.get_node_list()
        return node_list[node_id]

    def set_node(self, node: "BaseNode"):
        node_id = node.get_id()
        # print("to set node id:", node_id)

        # 初始化 node_list，如果尚不存在的话
        if self.ctx_key_node_list not in self.context:
            self.context[self.ctx_key_node_list] = {}

        self.context[self.ctx_key_node_list][node_id] = node
        # print("current node list:", self.context)
