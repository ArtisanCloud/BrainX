from enum import Enum

from sqlalchemy import (
    UUID,
    String,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import settings
from app.models.base import (
    BaseORM,
    table_name_provider_model,
    table_name_tenant,
    table_name_provider, table_name_provider_model_setting,
)


# Tenant's models provider
class ProviderModel(BaseORM):
    __tablename__ = table_name_provider_model
    __table_args__ = {"schema": settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public." + table_name_tenant + ".uuid"),
        nullable=False,
    )
    # provider_uuid = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey(settings.database.db_schema + "." + table_name_provider + ".uuid"),
    #     nullable=True,
    # )
    provider_name = mapped_column("provider_name", String, nullable=False)
    model_name = mapped_column("model_name", String, nullable=False)
    model_type = mapped_column("model_type", String, nullable=False)
    encrypted_config = mapped_column("encrypted_config", Text)
    is_valid = mapped_column("is_valid", Boolean, nullable=False, default=False)

    tenant: Mapped["Tenant"] = relationship(back_populates="model_providers")
    app_model_config: Mapped["AppModelConfig"] = relationship(
        back_populates="model_provider",
        foreign_keys="[AppModelConfig.model_provider_uuid]",
    )


class ProviderModelSetting(BaseORM):
    __tablename__ = table_name_provider_model_setting
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("public." + table_name_tenant + '.uuid'), index=True)
    provider_name = mapped_column(String(255), nullable=False)
    model_name = mapped_column(String(255), nullable=False)
    model_type = mapped_column(String(40), nullable=False)
    enabled = mapped_column(Boolean, nullable=False, default=True)
    load_balancing_enabled = mapped_column(Boolean, nullable=False, default=False)
