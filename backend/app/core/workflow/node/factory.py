from app.core.workflow.node.base import BaseNode, NodeType
from app.core.workflow.node.end.node import EndNode
from app.core.workflow.node.knowledge.node import KnowledgeNode
from app.core.workflow.node.llm.node import LLMNode
from app.core.workflow.node.plugin.node import PluginNode
from app.core.workflow.node.start.node import StartNode


class NodeFactory:
    @staticmethod
    def create_node(node_data: dict) -> BaseNode:
        try:
            node_type = node_data.get("node_type", "")
            match node_type:
                case NodeType.START.value:
                    return StartNode(node_data)
                case NodeType.END.value:
                    return EndNode(node_data)
                case NodeType.PLUGIN.value:
                    return PluginNode(node_data)
                case NodeType.KNOWLEDGE.value:
                    return KnowledgeNode(node_data)
                case NodeType.LLM.value:
                    return LLMNode(node_data)
                # 添加更多类型的 Node
                case _:
                    raise Exception(f"Unknown node type: {node_type}")
        except Exception as e:
            raise e
