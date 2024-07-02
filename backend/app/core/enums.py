from enum import Enum


class EnumWithValueOf(Enum):
    @classmethod
    def from_value(cls, value: str) -> 'Enum':
        """
        Get Enum member from given value.

        :param value: enum member value
        :return: enum member
        """
        for enum_member in cls:
            if enum_member.value == value:
                return enum_member
        raise ValueError(f'invalid enum value {value}')