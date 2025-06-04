from decimal import Decimal
from enum import Enum, StrEnum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.core.brainx.entity.base import I18nObject


class ModelType(Enum):
    """
    Enum class for different model types.
    """

    LLM = "llm"
    EMBEDDING = "embedding"
    TEXT_EMBEDDING = "text-embedding"
    IMAGE_EMBEDDING = "image-embedding"
    RERANK = "rerank"
    SPEECH2TEXT = "speech2text"
    MODERATION = "moderation"
    TTS = "tts"
    TEXT2IMG = "text2img"
    IMG2IMG = "img2img"
    TEXT2VIDEO = "text2video"


class FetchFrom(Enum):
    PREDEFINED_MODEL = "predefined-model"
    CUSTOMIZABLE_MODEL = "customizable-model"


class ModelFeature(Enum):
    TOOL_CALL = "tool-call"
    MULTI_TOOL_CALL = "multi-tool-call"
    AGENT_THOUGHT = "agent-thought"
    VISION = "vision"
    STREAM_TOOL_CALL = "stream-tool-call"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    STRUCTURED_OUTPUT = "structured-output"


class DefaultParameterName(StrEnum):
    """
    Enum class for parameter template variable.
    """

    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    TOP_K = "top_k"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    MAX_TOKENS = "max_tokens"
    RESPONSE_FORMAT = "response_format"
    JSON_SCHEMA = "json_schema"

    @classmethod
    def value_of(cls, value: Any) -> "DefaultParameterName":
        """
        Get parameter name from value.

        :param value: parameter value
        :return: parameter name
        """
        for name in cls:
            if name.value == value:
                return name
        raise ValueError(f"invalid parameter name {value}")


class ParameterType(Enum):
    """
    Enum class for parameter type.
    """

    FLOAT = "float"
    INT = "int"
    STRING = "string"
    BOOLEAN = "boolean"
    TEXT = "text"


class ModelPropertyKey(Enum):
    MODE = "mode"
    CONTEXT_SIZE = "context_size"
    MAX_CHUNKS = "max_chunks"
    FILE_UPLOAD_LIMIT = "file_upload_limit"
    SUPPORTED_FILE_EXTENSIONS = "supported_file_extensions"
    MAX_CHARACTERS_PER_CHUNK = "max_characters_per_chunk"
    DEFAULT_VOICE = "default_voice"
    VOICES = "voices"
    WORD_LIMIT = "word_limit"
    AUDIO_TYPE = "audio_type"
    MAX_WORKERS = "max_workers"
    ARCHITECTURE = "architecture"
    EMBEDDINGS_SIZE = "embeddings_size"
    LANGUAGES_SUPPORTED = "languages_supported"
    POOLING = "pooling"
    MAX_SEQUENCE_LENGTH = "max_sequence_length"


class ProviderModel(BaseModel):
    """
    Model class for provider model.
    """

    model: str
    label: I18nObject
    model_type: ModelType
    features: Optional[list[ModelFeature]] = None
    fetch_from: Optional[FetchFrom] = None
    model_properties: dict[ModelPropertyKey, Any]
    deprecated: bool = False
    model_config = ConfigDict(protected_namespaces=())


class ParameterRule(BaseModel):
    """
    Model class for parameter rule.
    """

    name: str
    use_template: Optional[str] = None
    label: Optional[I18nObject] = None
    type: Optional[ParameterType] = None
    help: Optional[I18nObject] = None
    required: bool = False
    default: Optional[Any] = None
    min: Optional[float] = None
    max: Optional[float] = None
    precision: Optional[int] = None
    options: list[str] = []


class PriceConfig(BaseModel):
    """
    Model class for pricing info.
    """

    input: Decimal
    output: Optional[Decimal] = None
    unit: Decimal
    currency: str


class AIModelEntity(ProviderModel):
    """
    Model class for AI model.
    """

    parameter_rules: list[ParameterRule] = []
    pricing: Optional[PriceConfig] = None


class ModelUsage(BaseModel):
    pass


class PriceType(Enum):
    """
    Enum class for price type.
    """

    INPUT = "input"
    OUTPUT = "output"


class PriceInfo(BaseModel):
    """
    Model class for price info.
    """

    unit_price: Decimal
    unit: Decimal
    total_amount: Decimal
    currency: str
