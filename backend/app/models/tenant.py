import hashlib
import uuid

from sqlalchemy import Column, String, Text, SmallInteger, UUID, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from app.models.base import BaseModel, table_name_tenant, table_name_tenant_default_model


# class Tenant(BaseModel):
class Tenant(BaseModel):
    __tablename__ = table_name_tenant

    name = mapped_column('name', String, nullable=False, unique=True)
    plan = mapped_column('plan', SmallInteger)
    status = mapped_column('status', SmallInteger)
    encrypted_public_key = mapped_column('encrypted_public_key', Text)
    config = mapped_column('config', Text)

    # users = relationship("User", secondary="pivot_tenant_to_user")
    apps = relationship("App")

    def __repr__(self):
        return (
            f"<Tenant(id={self.id}, "
            f"name='{self.name}', "
            f"plan={self.plan}, "
            f"status={self.status}, "
            f"encrypted_public_key='{self.encrypted_public_key[:10]}...', "
            f"config='{self.config[:10]}...')>"
        )


def generate_uuid(self):
    str_merged_uuid = self.user_uuid + self.tenant_uuid

    # 使用 SHA-256 哈希函数计算合并后的字符串的摘要
    hash_object = hashlib.sha256()
    hash_object.update(str_merged_uuid.encode())
    hash_digest = hash_object.digest()

    # 取摘要的前16字节作为UUID的字节序列
    uuid_bytes = hash_digest[:16]

    # 将哈希摘要转换为 UUID
    generated_uuid = uuid.UUID(bytes=uuid_bytes)

    return generated_uuid


class TenantDefaultModel(BaseModel):
    __tablename__ = table_name_tenant_default_model

    tenant_uuid = mapped_column('tenant_uuid', ForeignKey(table_name_tenant + '.uuid'), nullable=False)
    provider_name = mapped_column('provider_name', String(40), nullable=False)
    name = mapped_column('name', String(255), nullable=False)
    type = mapped_column('type', String(40), nullable=False)
