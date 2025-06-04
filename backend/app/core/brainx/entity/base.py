import re
from typing import Optional

from pydantic import BaseModel, model_validator, field_validator


# 定义支持多语言的字段对象
class I18nObject(BaseModel):
    zh_Hans: Optional[str] = None  # 中文字段，可选，默认为 None
    en_US: str  # 英文字段，必填

    # 使用 @model_validator 来进行模型级别的验证
    @model_validator(mode="before")
    def set_default_zh_Hans(cls, values):
        if "zh_Hans" not in values or not values["zh_Hans"]:
            values["zh_Hans"] = values["en_US"]
        return values

    # 使用 @field_validator 来验证字段类型
    @field_validator("en_US", "zh_Hans")
    def ensure_string(cls, value):
        if isinstance(value, str):
            return value
        raise ValueError("Value must be a string")


# 定义表单字段类型的枚举


# 定义表单显示条件的对象


# 定义表单选项的对象


class GenericProviderID:
    organization: str
    plugin_name: str
    provider_name: str
    is_hardcoded: bool

    def to_string(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.organization}/{self.plugin_name}/{self.provider_name}"

    def __init__(self, value: str, is_hardcoded: bool = False) -> None:
        if not value:
            raise Exception("plugin not found, please add plugin")
        # check if the value is a valid plugin id with format: $organization/$plugin_name/$provider_name
        if not re.match(r"^[a-z0-9_-]+\/[a-z0-9_-]+\/[a-z0-9_-]+$", value):
            # check if matches [a-z0-9_-]+, if yes, append with brainx/$value/$value
            if re.match(r"^[a-z0-9_-]+$", value):
                value = f"brainx/{value}/{value}"
            else:
                raise ValueError(f"Invalid plugin id {value}")

        self.organization, self.plugin_name, self.provider_name = value.split("/")
        self.is_hardcoded = is_hardcoded

    @property
    def plugin_id(self) -> str:
        return f"{self.organization}/{self.plugin_name}"


class ModelProviderID(GenericProviderID):
    def __init__(self, value: str, is_hardcoded: bool = False) -> None:
        super().__init__(value, is_hardcoded)
