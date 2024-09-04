from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from enum import Enum

from pydantic import BaseModel, Field

from app.core.workflow.context.manager import ContextManager
from app.core.workflow.node_variable.base import BaseNodeVariable
from app.core.workflow.state import GraphState


class NodeType(Enum):
    AGENT = ("agent_bot", "agent_bot", "Agent Node")
    START = ("start_input", "start", "Start Node")
    END = ("end_result", "end", "End Node")
    PLUGIN = ("plugin", "plugin", "Plugin Node")
    LLM = ("llm", "llm", "LLM Node")
    CODE = ("code", "code", "Code Node")
    KNOWLEDGE = ("knowledge", "knowledge", "Knowledge Node")
    WORKFLOW = ("workflow", "workflow", "Workflow Node")
    CONDITION = ("condition", "condition", "Condition Node")
    loop = ("loop", "loop", "Loop Node")
    INTENT_RECOGNITION = ("intent_recognition", "intent_recognition", "Intent Recognition Node")
    TEXT_PROCESSING = ("text_processing", "text_processing", "Text Processing Node")
    MESSAGE = ("message", "message", "Message Node")
    QUESTION = ("question", "question", "Question Node")
    VARIABLE = ("variable", "variable", "Variable Node")
    DATABASE = ("database", "database", "Database Node")

    def __init__(self, id: str, type: str, name: str):
        self._id = id
        self._type = type
        self._name = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> str:
        return self._name


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
