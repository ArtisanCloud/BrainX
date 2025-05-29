from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel

from app.core.brainx.entity.base import I18nObject
from app.models.model_provider.provider_model import ModelType


class ModelFeature(Enum):
    """
    Enum class for llm feature.
    """

    TOOL_CALL = "tool-call"
    MULTI_TOOL_CALL = "multi-tool-call"
    AGENT_THOUGHT = "agent-thought"
    VISION = "vision"
    STREAM_TOOL_CALL = "stream-tool-call"


class FetchFrom(Enum):
    PREDEFINED = "predefined-model"
    CUSTOMIZED = "customizable-model"


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


class ProviderModelEntity(BaseModel):
    """
    Model class for provider model_provider.
    """

    model: str
    label: I18nObject
    model_type: ModelType
    features: Optional[list[ModelFeature]] = None
    fetch_from: Optional[FetchFrom] = None
    model_properties: dict[ModelPropertyKey, Any]
    deprecated: bool = False

    class Config:
        protected_namespaces = ()
