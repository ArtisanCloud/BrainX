from abc import ABC
from enum import Enum

from app.core.enums import EnumWithValueOf


class BaseNode(ABC):
    tenant_uuid: str
    app_uuid: str
    workflow_uuid: str


class NodeType(EnumWithValueOf):
    CODE = "code"
    CONDITION = "condition"
    DATABASE = "database"
    END = "end"
    KNOWLEDGE = "knowledge"
    LLM = "llm"
    MESSAGE = "message"
    START = "start"
    SUB_WORKFLOW = "sub_workflow"
    TEXT_PROCESS = "text_process"
    TOOL = "tool"
    VARIABLE = "variable"
