from enum import Enum
from typing import Optional, Sequence, List

from pydantic import BaseModel, ConfigDict, Field

from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.runtime.provider_model import ModelType, AIModelEntity


class ConfigurateMethod(Enum):
    """
    枚举类，用于定义提供者模型的配置方法。
    """

    PREDEFINED_MODEL = "predefined-model"  # 预定义模型
    CUSTOMIZED_MODEL = "customizable-model"  # 自定义模型


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


class FormShowOnObject(BaseModel):
    """
    Model class for defining when a form field should be shown.
    用于定义表单字段何时显示的模型类，通过变量名和值的匹配进行控制。
    """

    variable: str  # 变量名称
    value: str  # 当变量的值匹配时，显示该字段


class FormOption(BaseModel):
    """
    Model class for form options.
    用于定义表单选项的模型类，包含选项的标题、多语言支持、值及其显示条件。
    """

    label: I18nObject  # 选项标题，支持多语言
    value: str  # 选项值
    show_on: list[FormShowOnObject] = []  # 选项显示条件，默认为空列表

    def __init__(self, **data):
        super().__init__(**data)
        # 如果没有提供标题，默认使用选项值作为标题
        if not self.label:
            self.label = I18nObject(en_US=self.value)


class CredentialFormSchema(BaseModel):
    """
    Model class for credential form schema.
    """

    variable: str
    label: I18nObject
    type: FormType
    required: bool = True
    default: Optional[str] = None
    options: Optional[list[FormOption]] = None
    placeholder: Optional[I18nObject] = None
    max_length: int = 0
    show_on: list[FormShowOnObject] = []


class ProviderCredentialSchema(BaseModel):
    credential_form_schemas: list[CredentialFormSchema]


class FieldModelSchema(BaseModel):
    label: I18nObject
    placeholder: Optional[I18nObject] = None


class ModelCredentialSchema(BaseModel):
    model: FieldModelSchema
    credential_form_schemas: list[CredentialFormSchema]


class SimpleProviderEntity(BaseModel):
    """
    Simple model class for provider.
    """

    provider: Optional[str] = None
    label: Optional[I18nObject] = None
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    supported_model_types: Sequence[ModelType]
    models: list[AIModelEntity] = []


class ProviderHelpEntity(BaseModel):
    """
    帮助信息模型，包含帮助标题和链接。
    """

    label: I18nObject  # 帮助标题，支持多语言
    url: I18nObject  # 帮助链接，必须是有效的URL


class ProviderEntity(BaseModel):
    """
    提供者模式定义，描述提供者的详细信息、支持的模型类型、配置方法等。
    """
    provider: str
    label: I18nObject
    description: Optional[I18nObject] = None
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    background: Optional[str] = None
    help: Optional[ProviderHelpEntity] = None
    supported_model_types: Sequence[ModelType]
    configurate_methods: list[ConfigurateMethod]
    models: list[AIModelEntity] = Field(default_factory=list)
    provider_credential_schema: Optional[ProviderCredentialSchema] = None
    model_credential_schema: Optional[ModelCredentialSchema] = None

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())

    # position from plugin _position.yaml
    position: Optional[dict[str, list[str]]] = {}


class ProviderConfig(BaseModel):
    """
    Model class for provider config.
    """

    provider: str
    credentials: dict
