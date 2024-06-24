from sqlalchemy import Column, UUID, String, Text, Boolean, SmallInteger, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseModel, table_name_model_provider, table_name_tenant


# Tenant's model provider
class ModelProvider(BaseModel):
    __tablename__ = table_name_model_provider

    tenant_uuid = mapped_column('tenant_uuid', ForeignKey(table_name_tenant + '.uuid'), nullable=False, index=True)
    name = mapped_column('name', String, nullable=False)
    model_name = mapped_column('model_name', String, nullable=False)
    model_type = mapped_column('model_type', String, nullable=False)
    encrypted_config = mapped_column('encrypted_config', Text)
    is_valid = mapped_column('is_valid', Boolean, nullable=False, default=False)
    last_used = mapped_column('last_used', TIMESTAMP(timezone=True), nullable=True)

    quota_type = mapped_column('quota_type', SmallInteger)
    quota_limit = mapped_column('quota_limit', BigInteger, nullable=True)
    quota_used = mapped_column('quota_used', BigInteger, default=0)

    # tenant = relationship("Tenant", backref="model_providers")
    app_model_configs:Mapped["AppModelConfig"] = relationship( backref="model_provider")
