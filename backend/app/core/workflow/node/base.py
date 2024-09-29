from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypedDict

from enum import Enum

from pydantic import BaseModel, Field

from app.core.workflow.context.manager import ContextManager
from app.core.workflow.node_variable.base import BaseNodeVariable
from app.core.workflow.state import GraphState


class NodeInfo(BaseModel):
    id: str
    type: str
    name: str
    icon: str
    description: str
    support_batch: bool


class NodeType(Enum):
    AGENT = "agent_bot"
    START = "start_input"
    END = "end_result"
    PLUGIN = "plugin"
    LLM = "llm"
    CODE = "code"
    KNOWLEDGE = "knowledge"
    WORKFLOW = "workflow"
    CONDITION = "condition"
    LOOP = "loop"
    INTENT_RECOGNITION = "intent_recognition"
    TEXT_PROCESSING = "text_processing"
    MESSAGE = "message"
    QUESTION = "question"
    VARIABLE = "variable"
    DATABASE = "database"


class BaseNode(ABC, BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # node info
    id: str
    name: str
    description: str = ""
    node_type: str = "start"  # Assume NodeType has a string representation

    position_x: float = 0.0
    position_y: float = 0.0
    width: float = 480.0
    height: float = 480.0
    next_nodes: List[str] = Field([])

    # dataset info
    dataset: Any = None
    llm: Any = None

    """
    This class represents the state for each node in the graph.
    It holds input and output data that can be shared across nodes.
    """
    input_vars: Dict[str, BaseNodeVariable] = Field(default_factory=dict)
    output_vars: Dict[str, BaseNodeVariable] = Field(default_factory=dict)
    context_manager: ContextManager = None

    def __init__(self, node_data: dict):
        super().__init__(**node_data)  # Ensure that the parent's __init__ method is called
        # self.id = node_data.get("id", "")
        # self.name = node_data.get("name", "")
        # self.llm = node_data.get("llm", None)
        # self.dataset = node_data.get("dataset", None)
        self._init_inputs(self.id, node_data.get("inputs", []))

    def _init_inputs(self, node_id, input_data):
        if input_data:
            for var in input_data:
                self.set_input(node_id, var)

    def set_context_manager(self, context_manager: ContextManager):
        self.context_manager = context_manager

    def get_context_value(self, key: str) -> Any:
        if self.context_manager:
            return self.context_manager.get(key)
        return None

    def set_context_value(self, key: str, value: Any):
        if self.context_manager:
            self.context_manager.set(key, value)

    @abstractmethod
    def execute(self, state: GraphState):
        print(f"~~~ "
              f"{self.name}: "
              # f"message: {state.messages}, "
              # f"context nodes length: {len(self.context_manager.get_node_list())}"
              f"~~~")

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_input(self, key: str, value: Any):
        self.input_vars[key] = value

    def get_input(self, key: str) -> Any:
        return self.input_vars.get(key)

    def set_output(self, key: str, value: Any):
        self.output_vars[key] = value

    def get_output(self, key: str) -> Any:
        return self.output_vars.get(key)

    def set_llm(self, llm: Any):
        self.llm = llm

    def to_dict(self):
        return self.dict(exclude_unset=True)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


# 定义节点信息
node_info_list: List[NodeInfo] = [
    NodeInfo(id="plugin", type=NodeType.PLUGIN.value, name="插件",
             icon="plugin",  # icon_key
             description="Integrates external plugins.", support_batch=True),

    NodeInfo(id="llm", type=NodeType.LLM.value, name="LLM",
             icon="llm",  # icon_key
             description="Invoke the large language model, generate responses using variables and prompt words.",
             support_batch=True),

    NodeInfo(id="code", type=NodeType.CODE.value, name="代码",
             icon="code",  # icon_key
             description="Executes custom code snippets.", support_batch=True),

    NodeInfo(id="knowledge", type=NodeType.KNOWLEDGE.value, name="知识库",
             icon="knowledge",  # icon_key
             description="Handles knowledge base interactions.", support_batch=False),

    NodeInfo(id="workflow", type=NodeType.WORKFLOW.value, name="工作流",
             icon="workflow",  # icon_key
             description="Invokes another workflow.", support_batch=True),

    NodeInfo(id="condition", type=NodeType.CONDITION.value, name="条件",
             icon="condition",  # icon_key
             description="Evaluates conditions to control workflow flow.", support_batch=False),

    NodeInfo(id="loop", type=NodeType.LOOP.value, name="循环",
             icon="loop",  # icon_key
             description="Handles looping logic within the workflow.", support_batch=True),

    NodeInfo(id="intent_recognition", type=NodeType.INTENT_RECOGNITION.value, name="认知度",
             icon="intent_recognition",  # icon_key
             description="Recognizes user intents.", support_batch=False),

    NodeInfo(id="text_processing", type=NodeType.TEXT_PROCESSING.value, name="文本处理",
             icon="text_processing",  # icon_key
             description="Processes and manipulates text.", support_batch=True),

    NodeInfo(id="message", type=NodeType.MESSAGE.value, name="消息",
             icon="message",  # icon_key
             description="Sends or receives messages.", support_batch=False),

    NodeInfo(id="question", type=NodeType.QUESTION.value, name="问题",
             icon="question",  # icon_key
             description="Handles question and answer interactions.", support_batch=False),

    NodeInfo(id="variable", type=NodeType.VARIABLE.value, name="变量",
             icon="variable",  # icon_key
             description="Manages variables within the workflow.", support_batch=True),

    NodeInfo(id="database", type=NodeType.DATABASE.value, name="数据库",
             icon="database",  # icon_key
             description="Interacts with the database.", support_batch=True),
]
