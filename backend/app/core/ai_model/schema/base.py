from enum import Enum
from typing import Optional

from pydantic import BaseModel, model_validator, field_validator


# 定义支持多语言的字段对象
class MultilingualField(BaseModel):
    zh_CN: Optional[str] = None  # 中文字段，可选，默认为 None
    en_US: str  # 英文字段，必填

    # 使用 @model_validator 来进行模型级别的验证
    @model_validator(mode="before")
    def set_default_zh_CN(cls, values):
        if "zh_CN" not in values or not values["zh_CN"]:
            values["zh_CN"] = values["en_US"]
        return values

    # 使用 @field_validator 来验证字段类型
    @field_validator("en_US", "zh_CN")
    def ensure_string(cls, value):
        if isinstance(value, str):
            return value
        raise ValueError("Value must be a string")


# 定义表单字段类型的枚举
class FormType(Enum):
    """
    Enum class for different types of form fields.
    定义表单字段类型的枚举类，包括文本输入、密码输入、选择、单选按钮和开关。
    """

    INPUT_TEXT = "text-input"  # 文本输入
    INPUT_SECRET = "secret-input"  # 密码输入
    SELECT = "select"  # 选择列表
    RADIO = "radio"  # 单选按钮
    SWITCH = "switch"  # 开关


# 定义表单显示条件的对象
class FormShowOnObject(BaseModel):
    """
    Model class for defining when a form field should be shown.
    用于定义表单字段何时显示的模型类，通过变量名和值的匹配进行控制。
    """

    variable: str  # 变量名称
    value: str  # 当变量的值匹配时，显示该字段


# 定义表单选项的对象
class FormOption(BaseModel):
    """
    Model class for form options.
    用于定义表单选项的模型类，包含选项的标题、多语言支持、值及其显示条件。
    """

    title: MultilingualField  # 选项标题，支持多语言
    value: str  # 选项值
    show_on: list[FormShowOnObject] = []  # 选项显示条件，默认为空列表

    def __init__(self, **data):
        super().__init__(**data)
        # 如果没有提供标题，默认使用选项值作为标题
        if not self.title:
            self.title = MultilingualField(en_US=self.value)
