import io
import logging
from typing import List, Dict, Literal, Type

from PIL import Image as PILImage
from langchain_core.prompts import ChatPromptTemplate

from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolInvocation
from pydantic import BaseModel, Field

from app import settings
from app.core.brain.llm.langchain import get_openai_llm
from app.core.workflow.graph import Graph
from app.core.workflow.node.base import NodeType
from app.core.workflow.node.factory import NodeFactory
from app.core.workflow.node.knowledge.node import KnowledgeNode
from app.core.workflow.node.plugin.node import PluginNode
from app.core.workflow.state import GraphState
from app.models import AppModelConfig, App


def create_dynamic_route_query(options: list[str]) -> Type[BaseModel]:
    """Dynamically create a RouteQuery model with a dynamic Literal."""

    class DynamicRouteQuery(BaseModel):
        route_to: Literal[tuple(options)] = Field(
            ...,
            description="Given a user question choose to route it to one of the available options.",
        )

    return DynamicRouteQuery


class AgentBot:
    def __init__(self, app: App = None, app_model_config: AppModelConfig = None):
        # graph
        self.builder = None
        self.graph = None
        self.llm = None
        self.router = None
        self.routes_options = []

        # persona
        self.persona = ""

        # Skills
        self.plugins: List[PluginNode] = []
        self.workflows: List[Graph] = []
        self.Triggers: List[ToolInvocation] = []

        # Knowledge
        self.text_datasets: List[KnowledgeNode] = []
        self.table_datasets: List[KnowledgeNode] = []
        self.image_datasets: List[KnowledgeNode] = []

        # Memory
        self.variables: List[Dict[str: str]] = []
        self.databases: List[dict] = []
        self.long_term_memory: bool = False
        self.filebox = False

        # Chat Experience
        self.auto_suggestion = False

        # Role
        self.voices: List[dict] = []

        try:
            self.init_llm(app_model_config)
            self.init_plugins(app_model_config)
            self.init_text_datasets(app_model_config)
            # self.init_workflows()
            self.init_router(app_model_config)

            self.build()

        except Exception as e:
            raise e

    def init_llm(self, app_model_config: AppModelConfig):

        self.llm = get_openai_llm("gpt-3.5-turbo", temperature=0, streaming=False)

    def init_plugins(self, app_model_config: AppModelConfig):
        self.plugins = [
            PluginNode({
                "id": "web_search",
                "name": "web search",
                "llm": self.llm
            }),
            PluginNode({
                "id": "local_tool",
                "name": "local tool",
                "llm": self.llm,
            }),
        ]
        for plugin in self.plugins:
            node_id = plugin.get_id()
            self.routes_options.append(node_id)

    def init_text_datasets(self, app_model_config: AppModelConfig):
        self.text_datasets = [
            KnowledgeNode({
                "id": "vectorstore_retrieve",
                "name": "vectorstore retrieve",
                "llm": self.llm,
            }),
            KnowledgeNode({
                "id": "table_retrieve",
                "name": "table retrieve",
                "llm": self.llm,
            }),
        ]
        for dataset in self.text_datasets:
            node_id = dataset.get_id()
            self.routes_options.append(node_id)

    def init_router(self, app_model_config: AppModelConfig):
        # print(self.routes_options)

        # 动态生成 RouteQuery 类
        route_query = create_dynamic_route_query(self.routes_options)
        structured_llm_router = self.llm.with_structured_output(route_query)

        self.persona = app_model_config.persona_prompt
        # print(self.persona)
        route_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.persona),
                ("human", "{question}"),
            ]
        )

        self.router = route_prompt | structured_llm_router
        # print(
        #     self.router.invoke(
        #         {"question": "Who will the Bears draft first in the NFL draft?"}
        #     )
        # )
        # print(self.router.invoke({"question": "What are the types of agent memory?"}))

    def agent_route(self, state: GraphState):
        print(f"---ROUTE QUESTION---: {state.question}")

        source = self.router.invoke({"question": state.question})

        # Check the type of `source`
        if isinstance(source, dict):
            route_to = source.get("route_to")
        else:
            route_to = getattr(source, "route_to", None)

        if route_to == "web_search":
            print("---ROUTE QUESTION TO WEB SEARCH---")
            return "web_search"
        elif route_to == "local_tool":
            print("---ROUTE QUESTION TO RAG---")
            return "local_tool"

        elif route_to == "vectorstore_retrieve":
            print("---ROUTE QUESTION TO RAG---")
            return "vectorstore_retrieve"
        elif route_to == "table_retrieve":
            print("---ROUTE QUESTION TO RAG---")
            return "table_retrieve"
        else:
            print("---ROUTE QUESTION UNKNOWN---")
            return None

    def call_agent(self, state: GraphState):
        messages = state.messages
        print(f"Calling agent with messages: {messages}")
        # self.llm = self.llm.bind_tools(self.tools)
        response = self.llm.invoke(messages)

        return {"messages": [response]}

    def build(self):
        try:
            self.builder = StateGraph(GraphState)
            generate_node = NodeFactory.create_node(
                {
                    "id": NodeType.END.id,
                    "name": "Generate",
                    "node_type": NodeType.END.type,
                    "llm": self.llm
                })
            self.builder.add_node(NodeType.END.id, generate_node.execute)

            routes = {}
            # add plugin nodes
            for plugin in self.plugins:
                node_id = plugin.get_id()
                self.builder.add_node(plugin.get_id(), lambda state: plugin.execute(state))
                routes[node_id] = node_id

            # add dataset nodes
            for dataset in self.text_datasets:
                node_id = dataset.get_id()
                self.builder.add_node(node_id, dataset.execute)
                routes[node_id] = node_id

            # add edges
            for route_option in self.routes_options:
                self.builder.add_edge(route_option, NodeType.END.id)

            # print(routes)
            self.builder.set_conditional_entry_point(
                self.agent_route,
                routes,
            )

            self.builder.add_edge(NodeType.END.id, END)
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
