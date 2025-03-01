import io
from typing import List, Dict, Literal, Type, Any

from PIL import Image as PILImage
from langchain_core.prompts import ChatPromptTemplate

from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolInvocation
from pydantic import BaseModel, Field

from app.config.config import settings
from app.core.brainx.base import LLMModel
from app.core.brainx.llm.langchain import get_llm
from app.core.rag.retrieval.interface import BaseRetriever
from app.core.workflow.graph import Graph
from app.core.workflow.node.base import NodeType
from app.core.workflow.node.factory import NodeFactory
from app.core.workflow.node.knowledge.node import (
    KnowledgeNode,
    KnowledgeNodeDatasetConfig,
)
from app.core.workflow.node.plugin.node import PluginNode
from app.core.workflow.state import GraphState
from app.logger import logger
from app.models import App


def create_dynamic_route_query(options: list[str]) -> Type[BaseModel]:
    """Dynamically create a RouteQuery model with a dynamic Literal."""

    class DynamicRouteQuery(BaseModel):
        route_to: Literal[tuple(options)] = Field(
            ...,
            description="Given a user question choose to route it to one of the available options.",
        )

    return DynamicRouteQuery


class AgentBot:
    def __init__(
            self,
            default_llm: str = LLMModel.BAIDU_ERNIE_Lite_8K.value,
            app: App = None,
            retriever: BaseRetriever = None,
    ):
        # graph
        self.builder = None
        self.graph: CompiledStateGraph | None = None
        self.default_llm = None
        self.router_llm = None
        self.generate_llm = None
        self.router = None
        self.routes_options = [NodeType.END.value]

        self.app = app
        self.retriever = retriever

        # Skills
        self.plugins: List[PluginNode] = []
        self.workflows: List[Graph] = []
        self.Triggers: List[ToolInvocation] = []

        # Knowledge
        self.text_datasets: List[KnowledgeNode] = []
        self.table_datasets: List[KnowledgeNode] = []
        self.image_datasets: List[KnowledgeNode] = []

        # Memory
        self.variables: List[Dict[str:str]] = []
        self.databases: List[dict] = []
        self.long_term_memory: bool = False
        self.filebox = False

        # Chat Experience
        self.auto_suggestion = False

        # Role
        self.voices: List[dict] = []

        try:
            self.init_llm(default_llm)
            # self.init_plugins()
            self.init_text_datasets()
            # self.init_workflows()
            self.init_router()

            self.build()

        except Exception as e:
            raise e

    def init_llm(self, default_llm: str = LLMModel.BAIDU_ERNIE_Lite_8K.value):
        # match self.app.current_app_model_config.model_provider:
        self.default_llm, exception = get_llm(
            default_llm, params={
                "temperature": 0,
                "streaming": False
            }
        )
        if exception:
            raise exception

        # 根据配置文件中的 router_llm 初始化 router_llm
        default_router_llm = LLMModel.OPENAI_GPT_3_D_5_TURBO.value
        if (
                settings.agent.router_llm == LLMModel.BAIDU_ERNIE_Lite_8K.value
                or settings.agent.router_llm == LLMModel.OLLAMA_LLAMA3_2.value
        ):
            default_router_llm = settings.agent.router_llm

        self.router_llm, exception = get_llm(
            default_router_llm,
            params={
                "temperature": 0,
                "streaming": False
            }
        )
        if exception:
            raise exception

        self.generate_llm, exception = get_llm(
            default_llm,
            params={
                "temperature": 0,
                "streaming": False
            }
        )
        if exception:
            raise exception

    def init_plugins(self):
        self.plugins = [
            PluginNode(
                {"id": "web_search", "name": "web search", "llm": self.default_llm}
            ),
            PluginNode(
                {
                    "id": "local_tool",
                    "name": "local tool",
                    "llm": self.default_llm,
                }
            ),
        ]
        for plugin in self.plugins:
            node_id = plugin.get_id()
            self.routes_options.append(node_id)

    def init_text_datasets(self):
        if hasattr(self.app, "connected_datasets") and self.app.connected_datasets:
            for dataset in self.app.connected_datasets:
                # use the dataset name as route id
                node_id = dataset.name
                # create the knowledge node
                knowledge = NodeFactory.create_node(
                    {
                        "id": node_id,
                        "name": dataset.name,
                        "node_type": NodeType.KNOWLEDGE.value,
                        "retriever": self.retriever,
                        "datasets": [dataset],
                        "config": KnowledgeNodeDatasetConfig(),
                    }
                )
                self.text_datasets.append(knowledge)

                # setup route options for route label
                self.routes_options.append(node_id)

    def init_router(self):
        logger.info("------route options:", self.routes_options)

        # 动态生成 RouteQuery 类
        route_query = create_dynamic_route_query(self.routes_options)
        structured_llm_router = self.router_llm.with_structured_output(route_query)

        persona = (
            self.app.persona
            if self.app.persona
            else "You are a helpful assistant. Answer all questions to the best of your ability."
        )
        route_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", persona),
                ("human", "{question}"),
            ]
        )

        self.router = route_prompt | structured_llm_router
        # logger.info(
        #     self.router.invoke(
        #         {"question": "Who will the Bears draft first in the NFL draft?"}
        #     )
        # )
        # logger.info(self.router.invoke({"question": "What are the types of agent memory?"}))

    def agent_route(self, state: GraphState):
        logger.info(f"---ROUTE QUESTION---: {state['question']}")

        # source = self.router.invoke({"question": state['question']})
        source = ""
        try:
            source = self.router.invoke({"question": state["question"]})
        except Exception as e:
            logger.error(f"invoke route:{e}", exc_info=False)

        logger.info(f"---SOURCE ROUTE TO---: {source}")
        # Check the type of `source`
        if isinstance(source, dict):
            route_to = source.get("route_to")
        else:
            route_to = getattr(source, "route_to", None)

        if route_to == "web_search":
            logger.info("---ROUTE QUESTION TO WEB SEARCH---")
            return "web_search"
        elif route_to == "local_tool":
            logger.info("---ROUTE QUESTION TO RAG---")
            return "local_tool"

        # 如果 route_to 在 self.text_datasets 的节点列表中，则动态执行对应的 KnowledgeNode
        text_dataset_ids = {dataset.get_id() for dataset in self.text_datasets}
        if route_to in text_dataset_ids:
            logger.info(f"---ROUTE QUESTION TO KNOWLEDGE NODE: {route_to} ---")
            return route_to

        elif route_to == "table_retrieve":
            logger.info("---ROUTE QUESTION TO RAG---")
            return "table_retrieve"
        else:
            logger.info("---ROUTE QUESTION UNKNOWN redirect to generate ---")
            return NodeType.END.value

    def call_agent(self, state: GraphState):
        messages = state["messages"]
        logger.info(f"Calling agent with messages: {messages}")
        # self.default_llm = self.default_llm.bind_tools(self.tools)
        response = self.default_llm.invoke(messages)

        return {"messages": [response]}

    def build(self):
        try:
            self.builder = StateGraph(GraphState)
            generate_node = NodeFactory.create_node(
                {
                    "id": NodeType.END.value,
                    "name": "Generate",
                    "node_type": NodeType.END.value,
                    "llm": self.generate_llm,
                    "app": self.app,
                }
            )
            self.builder.add_node(NodeType.END.value, generate_node.execute)
            # default generate node
            routes = {NodeType.END.value: NodeType.END.value}

            # add plugin nodes
            for plugin in self.plugins:
                node_id = plugin.get_id()
                self.builder.add_node(node_id, lambda state: plugin.execute(state))
                routes[node_id] = node_id

            # add dataset nodes
            for dataset in self.text_datasets:
                node_id = dataset.get_id()
                self.builder.add_node(node_id, dataset.execute)
                routes[node_id] = node_id

            # add edges
            for route_option in self.routes_options:
                if route_option == NodeType.END.value:
                    continue
                self.builder.add_edge(route_option, NodeType.END.value)

            # logger.info(routes)
            self.builder.set_conditional_entry_point(
                self.agent_route,
                routes,
            )

            self.builder.add_edge(NodeType.END.value, END)
            self.builder.set_finish_point(
                NodeType.END.value
            )  # Make sure this ID matches a node in the graph

            self.graph = self.builder.compile()

            # logger.info(self.graph)
        except Exception as e:
            raise Exception(f"Failed to build graph: {e}")

    def save_graph_image(self):
        try:
            # 获取 Mermaid 图形的 PNG 数据
            png_image = self.graph.get_graph().draw_mermaid_png()

            # 使用 io.BytesIO 将 PNG 数据流转换为一个 BytesIO 对象
            image_stream = io.BytesIO(png_image)

            # 使用 PIL 保存图像
            with PILImage.open(image_stream) as img:
                img.save("graph.png")  # 保存为 graph.png

            logger.info("Graph image saved as 'graph.png'.")

        except ValueError as e:
            logger.error(f"Failed to render graph: {e}")

    def run(self, initial_state: GraphState):
        # self.save_graph_image()
        # stream_response = self.graph.stream(initial_state)
        response = self.graph.invoke(initial_state)
        stream_response = response["result"]
        return stream_response


def create_graph_from_json(graph_data: dict) -> Graph:
    graph = Graph(graph_data)

    return graph
