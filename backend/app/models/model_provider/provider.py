from enum import Enum

from sqlalchemy import SmallInteger, BigInteger, TIMESTAMP, String, Boolean, UUID, ForeignKey, Text
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app import settings
from app.models.base import BaseORM, table_name_provider


class ProviderType(Enum):
    """
    Enum class for provider type.
    """
    SYSTEM = "system"  # 系统自带的提供者类型
    CUSTOM = "custom"  # 用户定义的提供者类型

class Provider(BaseORM):
    __tablename__ = table_name_provider
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    provider_name = mapped_column(String, nullable=False)
    provider_type = mapped_column(String, nullable=False)  # e.g., 'custom', 'system'
    encrypted_config = mapped_column(Text, nullable=True)
    is_valid = mapped_column(Boolean, nullable=False, default=False)
    last_used = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    quota_type = mapped_column(SmallInteger, nullable=True)  # e.g., PAID, FREE, TRIAL
    quota_limit = mapped_column(BigInteger, nullable=True)
    quota_used = mapped_column(BigInteger, default=0)

    # Relationships
    # model_providers = relationship("ProviderModel", back_populates="provider")

    def __repr__(self):
        return f"<Provider(id={self.id}, tenant_uuid={self.tenant_uuid}, provider_name='{self.provider_name}', provider_type='{self.provider_type}')>"
