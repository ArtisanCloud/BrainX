from enum import Enum

from sqlalchemy import Column, UUID, String, Text, Boolean, SmallInteger, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseORM, table_name_provider_model, table_name_tenant, table_name_provider


class ModelType(Enum):
    """
    Enum class for different model types.
    """
    LLM = "llm"
    EMBEDDING = "embedding"
    TEXT_EMBEDDING = "text_embedding"
    IMAGE_EMBEDDING = "image_embedding"
    RERANK = "rerank"
    SPEECH2TEXT = "speech2text"
    MODERATION = "moderation"
    TTS = "tts"
    TEXT2IMG = "text2img"
    IMG2IMG = "img2img"
    TEXT2VIDEO = "text2video"


# Tenant's models provider
class ProviderModel(BaseORM):
    __tablename__ = table_name_provider_model

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + ".uuid"), nullable=False)
    provider_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_provider + ".uuid"), nullable=True)
    model_name = mapped_column('model_name', String, nullable=False)
    model_type = mapped_column('model_type', String, nullable=False)
    encrypted_config = mapped_column('encrypted_config', Text)
    is_valid = mapped_column('is_valid', Boolean, nullable=False, default=False)


    tenant: Mapped["Tenant"] = relationship(back_populates="model_providers")
    app_model_config: Mapped["AppModelConfig"] = relationship(back_populates="model_provider",
                                                              foreign_keys="[AppModelConfig.model_provider_uuid]")
