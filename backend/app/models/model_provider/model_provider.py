from sqlalchemy import Column, UUID, String, Text, Boolean, SmallInteger, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseORM, table_name_model_provider, table_name_tenant


# Tenant's models provider
class ModelProvider(BaseORM):
    __tablename__ = table_name_model_provider

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + ".uuid"), nullable=False)
    name = mapped_column('name', String, nullable=False)
    model_name = mapped_column('model_name', String, nullable=False)
    model_type = mapped_column('model_type', String, nullable=False)
    encrypted_config = mapped_column('encrypted_config', Text)
    is_valid = mapped_column('is_valid', Boolean, nullable=False, default=False)
    last_used = mapped_column('last_used', TIMESTAMP(timezone=True), nullable=True)

    quota_type = mapped_column('quota_type', SmallInteger)
    quota_limit = mapped_column('quota_limit', BigInteger, nullable=True)
    quota_used = mapped_column('quota_used', BigInteger, default=0)

    tenant: Mapped["Tenant"] = relationship(back_populates="model_providers")
    app_model_config: Mapped["AppModelConfig"] = relationship(back_populates="model_provider",
                                                              foreign_keys="[AppModelConfig.model_provider_uuid]")
