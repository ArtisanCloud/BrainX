import io
from typing import Dict

from PIL import Image as PILImage
from langchain_core.messages import AIMessage

from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolExecutor

from app import settings
from app.core.brainx.base import LLMModel
from app.core.brainx.model_instance import ModelInstance
from app.core.workflow.context.manager import ContextManager
from app.core.workflow.node.base import NodeType
from app.core.workflow.node.factory import NodeFactory
from app.core.workflow.state import GraphState
from app.logger import logger


class Graph:
    llm_model_instance: ModelInstance

    def __init__(
            self,
            graph_data: Dict,
            llm_model_instance: ModelInstance = None,
    ):

        self.builder = None
        self.graph: CompiledStateGraph | None = None
        self.context_manager: ContextManager = ContextManager()  # Global context

        self.default_llm = llm_model_instance
        self.router_llm = llm_model_instance
        self.generate_llm = llm_model_instance
        self.router = None
        self.routes_options = [NodeType.END.value]
        self.tools = []
        try:
            # self._build_static_nodes()
            self.tool_executor = ToolExecutor(self.tools)
            self.build(graph_data)
        except Exception as e:
            raise e

    def call_agent(self, state: GraphState):
        messages = state["messages"]
        print(f"Calling agent with messages: {messages}")
        # print(f"llm: {self.llm}")
        self.default_llm = self.default_llm.bind_tools(self.tools)
        # response = self.llm.invoke(messages)
        response = AIMessage(content="test...")
        return {"messages": [response]}

    def _build_static_nodes(self):
        self.builder = StateGraph(GraphState)

        # Static nodes based on graph_json
        self.builder.add_node(
            NodeType.START.value, lambda state: None
        )  # You can define a specific method or logic here
        self.builder.add_node(NodeType.AGENT.value, self.call_agent)
        self.builder.add_node(
            NodeType.KNOWLEDGE.value, lambda state: None
        )  # Define specific methods as needed
        self.builder.add_node(
            NodeType.PLUGIN.value, lambda state: None
        )  # Define specific methods as needed
        self.builder.add_node(
            NodeType.END.value, lambda state: None
        )  # Define specific methods as needed

        # Define edges between nodes directly
        self.builder.add_edge(NodeType.START.value, NodeType.AGENT.value)
        self.builder.add_edge(NodeType.AGENT.value, NodeType.KNOWLEDGE.value)
        self.builder.add_edge(NodeType.KNOWLEDGE.value, NodeType.PLUGIN.value)
        self.builder.add_edge(NodeType.PLUGIN.value, NodeType.END.value)

        # Set entry point and finish point
        self.builder.set_entry_point(
            NodeType.START.value
        )  # Make sure this ID matches a node in the graph
        self.builder.set_finish_point(
            NodeType.END.value
        )  # Make sure this ID matches a node in the graph

        self.graph = self.builder.compile()

    def build(self, graph_data: dict):
        try:

            self.builder = StateGraph(GraphState)

            self.builder.add_node(NodeType.AGENT.value, self.call_agent)
            # print("llm:", self.llm)
            for node_data in graph_data["nodes"]:
                node = NodeFactory.create_node(
                    {
                        **node_data,
                        "llm": self.default_llm,
                        "context_manager": self.context_manager,
                    }
                )
                self.context_manager.set_node(node)
                self.builder.add_node(node.get_id(), node.execute)

            for edge_data in graph_data["edges"]:
                self.builder.add_edge(edge_data["source"], edge_data["target"])

            self.builder.add_edge(NodeType.AGENT.value, NodeType.START.value)
            self.builder.add_edge(NodeType.END.value, END)

            self.builder.set_entry_point(
                NodeType.AGENT.value
            )  # Make sure this ID matches a node in the graph
            self.builder.set_finish_point(
                NodeType.END.value
            )  # Make sure this ID matches a node in the graph

            self.graph = self.builder.compile()

            # print(self.graph)
        except Exception as e:
            logger.error(f"Failed to build graph: {e}", exc_info=settings.log.exc_info)

    def save_graph_image(self):
        try:
            # 获取 Mermaid 图形的 PNG 数据
            png_image = self.graph.get_graph().draw_mermaid_png()

            # 使用 io.BytesIO 将 PNG 数据流转换为一个 BytesIO 对象
            image_stream = io.BytesIO(png_image)

            # 使用 PIL 保存图像
            with PILImage.open(image_stream) as img:
                img.save("graph_test.png")  # 保存为 graph.png

            print("Graph image saved as 'graph_test.png'.")

        except ValueError as e:
            print(f"Failed to render graph: {e}")

    def run(self, initial_state: GraphState):
        self.save_graph_image()

        result = self.graph.invoke(initial_state)
        return result


def create_graph_from_json(graph_data: dict) -> Graph:
    graph = Graph(graph_data)

    return graph
