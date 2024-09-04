from pydantic import Field

from app.core.workflow.node_variable.array_var import ArrayNodeVariable
from app.core.workflow.node_variable.base import VariableType



class ArrayNumberNodeVariable(ArrayNodeVariable):
    type: VariableType = Field(default=VariableType.ARRAY_NUMBER)
