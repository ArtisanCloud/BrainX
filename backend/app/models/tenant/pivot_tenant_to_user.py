import uuid

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.base import BasePivotModel, table_name_user, table_name_pivot_tenant_to_user
from app.models.tenant.tenant import table_name_tenant


class PivotTenantToUser(BasePivotModel):
    __tablename__ = table_name_pivot_tenant_to_user
    # 合并 schema 和约束条件
    __table_args__ = (
        UniqueConstraint('tenant_uuid', 'user_uuid', name='uq_tenant_to_user'),
        {'schema': 'public'},  # 这里不应使用字典，而是使用约束
    )

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + ".uuid"), nullable=False)
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + ".uuid"), nullable=False)

    tenant: Mapped["Tenant"] = relationship(uselist=False, overlaps="tenants")
    user: Mapped["User"] = relationship(uselist=False, overlaps="users")

    def __repr__(self):
        return (
            f"<PivotTenantToUser(uuid={self.uuid}, "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"user_uuid='{self.user_uuid}')>"
        )
