from typing import Any, Type, Union, List, Dict

from pydantic import BaseModel, Field

from enum import Enum


class VariableType(Enum):
    INTEGER = ("Integer", int)
    BOOLEAN = ("Boolean", bool)
    NUMBER = ("Number", Union[int, float])
    STRING = ("String", str)
    OBJECT = ("Object", dict)
    ARRAY_STRING = ("Array<String>", List[str])
    ARRAY_BOOLEAN = ("Array<Boolean>", List[bool])
    ARRAY_INTEGER = ("Array<Integer>", List[int])
    ARRAY_NUMBER = ("Array<Number>", List[Union[int, float]])

    # ARRAY_OBJECT = ("Array<Object>", List[Dict])

    def __init__(self, label: str, py_type: Type):
        self.label = label
        self.py_type = py_type

    @property
    def type(self) -> Type:
        """Returns the Python type associated with the VariableType."""
        return self.py_type

    def __str__(self):
        return self.label


class InputType(Enum):
    INPUT = "input"
    REFERENCE = "reference"


class BaseNodeVariable(BaseModel):
    """
    Represents a variable within a Node, including its metadata and value.
    """
    id: str = Field(..., description="The id of the variable.")
    input_type: InputType = Field(InputType.INPUT.value, description="The type of the input.")
    variable_type: VariableType = Field(..., description="The type of the variable.")
    value: Any = Field(None, description="The value of the variable.")
    reference_var: Dict[str, "BaseNodeVariable"] = Field(None, description="The reference variable.")
    description: str = Field("", description="A description of the variable.")
    is_required: bool = Field(True, description="Indicates if the variable is required.")
    is_editable: bool = Field(True, description="Indicates if the variable is editable.")
