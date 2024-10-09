import io
import logging
from typing import Any

from PIL import Image as PILImage
from langchain_core.messages import AIMessage

from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import  ToolExecutor

from app import settings
from app.core.brainx.llm.langchain import get_openai_llm
from app.core.workflow.context.manager import ContextManager
from app.core.workflow.node.base import NodeType
from app.core.workflow.node.factory import NodeFactory
from app.core.workflow.state import GraphState
from app.logger import logger


class Graph:
    def __init__(self, graph_data: {}):

        self.builder = None
        self.graph = None
        self.context_manager: ContextManager = ContextManager()  # Global context

        self.llm: Any = None
        self.init_llm()
        # self._build_static_nodes()
        self.tools = []
        self.tool_executor = ToolExecutor(self.tools)
        self.build(graph_data)

    def init_llm(self):

        self.llm = get_openai_llm("gpt-3.5-turbo", temperature=0, streaming=False)

    def call_agent(self, state: GraphState):
        messages = state.messages
        print(f"Calling agent with messages: {messages}")
        # print(f"llm: {self.llm}")
        self.llm = self.llm.bind_tools(self.tools)
        # response = self.llm.invoke(messages)
        response = AIMessage(content="test...")
        return {"messages": [response]}

    def _build_static_nodes(self):
        self.builder = StateGraph(GraphState)

        # Static nodes based on graph_json
        self.builder.add_node(NodeType.START.id, lambda state: None)  # You can define a specific method or logic here
        self.builder.add_node(NodeType.AGENT.id, self.call_agent)
        self.builder.add_node(NodeType.KNOWLEDGE.id, lambda state: None)  # Define specific methods as needed
        self.builder.add_node(NodeType.PLUGIN.id, lambda state: None)  # Define specific methods as needed
        self.builder.add_node(NodeType.END.id, lambda state: None)  # Define specific methods as needed

        # Define edges between nodes directly
        self.builder.add_edge(NodeType.START.id, NodeType.AGENT.id)
        self.builder.add_edge(NodeType.AGENT.id, NodeType.KNOWLEDGE.id)
        self.builder.add_edge(NodeType.KNOWLEDGE.id, NodeType.PLUGIN.id)
        self.builder.add_edge(NodeType.PLUGIN.id, NodeType.END.id)

        # Set entry point and finish point
        self.builder.set_entry_point(NodeType.START.id)  # Make sure this ID matches a node in the graph
        self.builder.set_finish_point(NodeType.END.id)  # Make sure this ID matches a node in the graph

        self.graph = self.builder.compile()

    def build(self, graph_data: dict):
        try:

            self.builder = StateGraph(GraphState)

            self.builder.add_node(NodeType.AGENT.id, self.call_agent)
            # print("llm:", self.llm)
            for node_data in graph_data["nodes"]:
                node = NodeFactory.create_node({
                    **node_data,
                    "llm": self.llm,
                    "context_manager": self.context_manager,
                })
                self.context_manager.set_node(node)
                self.builder.add_node(node.get_id(), node.execute)

            for edge_data in graph_data["edges"]:
                self.builder.add_edge(edge_data["source"], edge_data["target"])

            self.builder.add_edge(NodeType.AGENT.id, NodeType.START.id)
            self.builder.add_edge(NodeType.END.id, END)

            self.builder.set_entry_point(NodeType.AGENT.id)  # Make sure this ID matches a node in the graph
            self.builder.set_finish_point(NodeType.END.id)  # Make sure this ID matches a node in the graph

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
                img.save('graph.png')  # 保存为 graph.png

            print("Graph image saved as 'graph.png'.")

        except ValueError as e:
            print(f"Failed to render graph: {e}")

    def run(self, initial_state: GraphState):
        # self.save_graph_image()

        self.graph.invoke(initial_state)


def create_graph_from_json(graph_data: dict) -> Graph:
    graph = Graph(graph_data)

    return graph
