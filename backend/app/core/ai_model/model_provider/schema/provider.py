from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

# 这些是你定义的依赖模块
from app.core.ai_model.model_provider.schema.base import MultilingualField, FormType, FormOption, FormShowOnObject
from app.core.ai_model.model_provider.schema.provider_model import ProviderModelSchema
from app.models.model_provider.provider_model import ModelType


# 定义帮助信息对象
class Help(BaseModel):
    """
    帮助信息模型，包含帮助标题和链接。
    """
    title: MultilingualField  # 帮助标题，支持多语言
    url: HttpUrl  # 帮助链接，必须是有效的URL


# 配置方法枚举
class ConfigurateMethod(Enum):
    """
    枚举类，用于定义提供者模型的配置方法。
    """
    PREDEFINED_MODEL = "predefined"  # 预定义模型
    CUSTOMIZED_MODEL = "customized"  # 自定义模型


# 凭证表单字段的定义
class CredentialFormSchema(BaseModel):
    """
    凭证表单字段的模型定义，描述每个字段的属性。
    """
    variable: str  # 字段变量名称
    label: MultilingualField  # 字段标签，支持多语言
    type: FormType  # 字段类型，使用 FormType 枚举
    required: bool = True  # 是否必填，默认为 True
    default: Optional[str] = None  # 默认值，可选
    options: Optional[List[FormOption]] = None  # 字段选项，用于选择类型字段
    placeholder: Optional[MultilingualField] = None  # 占位符，支持多语言
    max_length: int = 0  # 字段最大长度
    show_on: List[FormShowOnObject] = []  # 字段展示条件


# 提供者凭证的定义
class ProviderCredentialSchema(BaseModel):
    """
    提供者凭证模式定义，包含多个凭证表单字段。
    """
    credential_form_schemas: List[CredentialFormSchema]  # 凭证表单字段列表


# 模型字段的定义
class FieldModelSchema(BaseModel):
    """
    模型字段定义，描述模型字段的标题和可选的占位符。
    """
    title: MultilingualField  # 字段标题，支持多语言
    placeholder: Optional[MultilingualField] = None  # 占位符，支持多语言


# 模型凭证的定义
class ModelCredentialSchema(BaseModel):
    """
    模型凭证模式定义，包含模型字段和多个凭证表单字段。
    """
    model: FieldModelSchema  # 模型字段
    credential_form_schemas: List[CredentialFormSchema]  # 凭证表单字段列表


# 定义提供者的主结构
class ProviderSchema(BaseModel):
    """
    提供者模式定义，描述提供者的详细信息、支持的模型类型、配置方法等。
    """
    provider: str  # 提供者名称
    title: MultilingualField  # 提供者的标题，支持多语言
    description: Optional[MultilingualField]  # 提供者的描述，支持多语言
    icon_small: Optional[MultilingualField]  # 小图标路径，支持多语言
    icon_large: Optional[MultilingualField]  # 大图标路径，支持多语言
    background: str  # 背景颜色（HEX 格式）
    help: Help  # 帮助信息
    supported_model_types: List[ModelType]  # 支持的模型类型列表
    configurate_methods: List[ConfigurateMethod]  # 支持的配置方法列表
    models: List[ProviderModelSchema] = []  # 可用的模型列表，默认为空
    provider_credential_schema: Optional[ProviderCredentialSchema] = None  # 提供者凭证模式，可选
    model_credential_schema: Optional[ModelCredentialSchema] = None  # 模型凭证模式，可选

    class Config:
        validate_assignment = False
        extra = "allow"  # 允许额外字段，不验证