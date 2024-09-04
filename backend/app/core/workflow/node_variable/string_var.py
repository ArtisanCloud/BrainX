from pydantic import Field

from app.core.workflow.node_variable.base import BaseNodeVariable, VariableType

class StringNodeVariable(BaseNodeVariable):
    type: VariableType = Field(default=VariableType.STRING)
