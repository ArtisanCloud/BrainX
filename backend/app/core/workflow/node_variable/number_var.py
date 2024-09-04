from pydantic import Field

from app.core.workflow.node_variable.base import BaseNodeVariable, VariableType

class NumberNodeVariable(BaseNodeVariable):
    type: VariableType = Field(default=VariableType.NUMBER)

