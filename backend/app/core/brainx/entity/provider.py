from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

# 这些是你定义的依赖模块
from .base import I18nObject, FormType, FormOption, FormShowOnObject
from .provider_model import ProviderModelEntity
from app.models.model_provider.provider_model import ModelType


# 定义帮助信息对象
class Help(BaseModel):
    """
    帮助信息模型，包含帮助标题和链接。
    """

    label: I18nObject  # 帮助标题，支持多语言
    url: I18nObject  # 帮助链接，必须是有效的URL


# 配置方法枚举
class ConfigurateMethod(Enum):
    """
    枚举类，用于定义提供者模型的配置方法。
    """

    PREDEFINED_MODEL = "predefined-model"  # 预定义模型
    CUSTOMIZED_MODEL = "customizable-model"  # 自定义模型


# 凭证表单字段的定义
class CredentialFormEntity(BaseModel):
    """
    凭证表单字段的模型定义，描述每个字段的属性。
    """

    variable: str  # 字段变量名称
    label: I18nObject  # 字段标签，支持多语言
    type: FormType  # 字段类型，使用 FormType 枚举
    required: bool = True  # 是否必填，默认为 True
    default: Optional[str] = None  # 默认值，可选
    options: Optional[List[FormOption]] = None  # 字段选项，用于选择类型字段
    placeholder: Optional[I18nObject] = None  # 占位符，支持多语言
    max_length: int = 0  # 字段最大长度
    show_on: List[FormShowOnObject] = []  # 字段展示条件


# 提供者凭证的定义
class ProviderCredentialEntity(BaseModel):
    credential_form_schemas: List[CredentialFormEntity]  # 凭证表单字段列表


# 模型字段的定义
class FieldModelEntity(BaseModel):
    """
    模型字段定义，描述模型字段的标题和可选的占位符。
    """

    label: I18nObject  # 字段标题，支持多语言
    placeholder: Optional[I18nObject] = None  # 占位符，支持多语言


# 模型凭证的定义
class ModelCredentialEntity(BaseModel):
    """
    模型凭证模式定义，包含模型字段和多个凭证表单字段。
    """

    model: FieldModelEntity  # 模型字段
    credential_form_schemas: List[CredentialFormEntity]  # 凭证表单字段列表


class ProviderQuotaType(Enum):
    PAID = "paid"
    """hosted paid quota"""

    FREE = "free"
    """third-party free quota"""

    TRIAL = "trial"
    """hosted trial quota"""

    @staticmethod
    def value_of(value):
        for member in ProviderQuotaType:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum found for value '{value}'")


class QuotaUnit(Enum):
    TIMES = "times"
    TOKENS = "tokens"
    CREDITS = "credits"


class SystemConfigurationStatus(Enum):
    """
    Enum class for system configuration status.
    """

    ACTIVE = "active"
    QUOTA_EXCEEDED = "quota-exceeded"
    UNSUPPORTED = "unsupported"


class RestrictModel(BaseModel):
    model: str
    base_model_name: Optional[str] = None
    model_type: ModelType

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())


class QuotaConfiguration(BaseModel):
    """
    Model class for provider quota configuration.
    """

    quota_type: ProviderQuotaType
    quota_unit: QuotaUnit
    quota_limit: int
    quota_used: int
    is_valid: bool
    restrict_models: list[RestrictModel] = []


class SystemConfiguration(BaseModel):
    """
    Model class for provider system configuration.
    """

    enabled: bool
    current_quota_type: Optional[ProviderQuotaType] = None
    quota_configurations: list[QuotaConfiguration] = []
    credentials: Optional[dict] = None


class CustomProviderConfiguration(BaseModel):
    """
    Model class for provider custom configuration.
    """

    credentials: dict


class CustomModelConfiguration(BaseModel):
    """
    Model class for provider custom model configuration.
    """

    model: str
    model_type: ModelType
    credentials: dict

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())


class CustomConfiguration(BaseModel):
    """
    Model class for provider custom configuration.
    """

    provider: Optional[CustomProviderConfiguration] = None
    models: list[CustomModelConfiguration] = []


class BaseProviderEntity(BaseModel):
    provider: str  # 提供者名称
    label: I18nObject  # 提供者的标题，支持多语言
    icon_small: Optional[I18nObject] = None  # 小图标路径，支持多语言
    icon_large: Optional[I18nObject] = None  # 大图标路径，支持多语言
    models: List[ProviderModelEntity] = []  # 可用的模型列表，默认为空


# 定义提供者的主结构
class ProviderEntity(BaseProviderEntity):
    """
    提供者模式定义，描述提供者的详细信息、支持的模型类型、配置方法等。
    """
    description: Optional[I18nObject] = None  # 提供者的描述，支持多语言
    background: str = None  # 背景颜色（HEX 格式）
    help: Help  # 帮助信息
    supported_model_types: List[ModelType]  # 支持的模型类型列表
    configurate_methods: List[ConfigurateMethod]  # 支持的配置方法列表
    provider_credential_schema: Optional[ProviderCredentialEntity] = None  # 提供者凭证模式，可选
    model_credential_schema: Optional[ModelCredentialEntity] = None  # 模型凭证模式，可选

    class Config:
        validate_assignment = False
        extra = "allow"  # 允许额外字段，不验证


class ProviderConfig(BaseModel):
    """
    Model class for provider config.
    """

    provider: str
    credentials: dict


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


class FieldModelSchema(BaseModel):
    label: I18nObject
    placeholder: Optional[I18nObject] = None


class CustomConfigurationStatus(Enum):
    ACTIVE = "active"
    NO_CONFIGURE = "no-configure"
