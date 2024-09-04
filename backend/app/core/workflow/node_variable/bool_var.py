from pydantic import Field

from app.core.workflow.node_variable.base import BaseNodeVariable, VariableType


class BooleanNodeVariable(BaseNodeVariable):
    type: VariableType = Field(default=VariableType.BOOLEAN)
