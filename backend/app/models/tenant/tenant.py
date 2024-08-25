from typing import List

from sqlalchemy import String, Text, SmallInteger, ForeignKey, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BaseORM, table_name_tenant, table_name_tenant_default_model, \
    table_name_pivot_tenant_to_user, table_name_user


# class Tenant(BaseORM):
class Tenant(BaseORM):
    __tablename__ = table_name_tenant

    name = mapped_column('name', String, nullable=False, unique=True)
    plan = mapped_column('plan', SmallInteger)
    status = mapped_column('status', SmallInteger)
    encrypted_public_key = mapped_column('encrypted_public_key', Text)
    config = mapped_column('config', Text)

    users: Mapped[List["User"]] = relationship(secondary=table_name_pivot_tenant_to_user,
                                               back_populates="tenants",
                                               overlaps="user, tenant"
                                               )
    owned_user: Mapped["User"] = relationship(back_populates="owned_tenant", foreign_keys='[User.tenant_owner_uuid]')
    apps: Mapped[List["App"]] = relationship(back_populates="tenant")
    model_providers: Mapped[List["ModelProvider"]] = relationship(back_populates="tenant")
    datasets: Mapped[List["Dataset"]] = relationship(back_populates="tenant",
                                                     foreign_keys="[Dataset.tenant_uuid]")

    def __repr__(self):
        return (
            f"<Tenant("
            # f"id={self.id}, "
            f"name='{self.name}', "
            f"plan={self.plan}, "
            f"status={self.status}, "
            f"encrypted_public_key='{self.encrypted_public_key[:10]}...', "
            f"config='{self.config[:10]}...')>"
        )


class TenantDefaultModel(BaseORM):
    __tablename__ = table_name_tenant_default_model

    tenant_uuid = mapped_column('tenant_uuid', ForeignKey(table_name_tenant + '.uuid'), nullable=False)
    provider_name = mapped_column('provider_name', String(40), nullable=False)
    name = mapped_column('name', String(255), nullable=False)
    type = mapped_column('type', String(40), nullable=False)
