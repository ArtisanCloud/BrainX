from typing import List

from sqlalchemy import Column, String, UUID, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseModel, table_name_app_model_config, table_name_model_provider


class AppModelConfig(BaseModel):
    __tablename__ = table_name_app_model_config

    app_uuid = mapped_column('app_uuid', UUID, nullable=False, index=True)
    model_provider_uuid = mapped_column('model_provider_uuid', ForeignKey(table_name_model_provider + '.uuid'),
                                        nullable=False, index=True)
    configs = mapped_column('configs', Text)
    persona_prompt = mapped_column('persona_prompt', Text)

    # app: Mapped["App"] = relationship(back_populates="model_config")
    # app_model_configs: Mapped[List["ModelProvider"]] = relationship(back_populates="app_model_configs")
