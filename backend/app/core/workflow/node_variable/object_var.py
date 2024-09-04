from typing import Any

from pydantic import Field

from app.core.workflow.node_variable.base import BaseNodeVariable, VariableType

class ObjectNodeVariable(BaseNodeVariable):
    type: VariableType = Field(default=VariableType.OBJECT)

    def get_value_by_key_path(self, key_path: str) -> Any:
        """
        Retrieve a value from the object by specifying a path.
        The path is a string of keys separated by dots.
        Example: "key1.key2.key3"
        """
        keys = key_path.split(".")
        current_value = self.value  # Assuming 'self.value' is a dict

        try:
            for key in keys:
                if isinstance(current_value, dict):
                    current_value = current_value[key]
                else:
                    raise ValueError(f"Cannot traverse through non-dict type at key '{key}'")
            return current_value
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            return None

    def set_value_by_key_path(self, key_path: str, new_value: Any) -> bool:
        """
        Set a value in the object by specifying a path.
        The path is a string of keys separated by dots.
        Example: "key1.key2.key3"
        """
        keys = key_path.split(".")
        current_value = self.value  # Assuming 'self.value' is a dict

        try:
            for key in keys[:-1]:
                if key not in current_value:
                    current_value[key] = {}
                current_value = current_value[key]
            current_value[keys[-1]] = new_value
            return True
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            return False