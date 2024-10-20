from typing import List

from sqlalchemy import Column, BigInteger, String, Text, DateTime, func, ForeignKey, SmallInteger, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app import settings
from app.models.base import BaseORM, table_name_workflow, table_name_app
from app.models.originaztion.user import table_name_user
from app.models.tenant.tenant import table_name_tenant


class Workflow(BaseORM):
    __tablename__ = table_name_workflow
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_tenant + ".uuid"), nullable=False)
    app_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(settings.database.db_schema+"." +table_name_app + ".uuid"), nullable=False)
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_user + '.uuid'), nullable=True)
    parent_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(settings.database.db_schema+"." +table_name_workflow + '.uuid'))

    name = mapped_column('name', String, nullable=False)
    tag = mapped_column('tag', String, nullable=False)
    description = mapped_column('description', Text)
    type = mapped_column('type', SmallInteger)
    graph = mapped_column('graph', Text)  # Using Text for JSON data
    meta = mapped_column('meta', Text)  # Using Text for JSON data

    app: Mapped[List["App"]] = relationship(back_populates="workflow", foreign_keys="[App.workflow_uuid]")

    def __repr__(self):
        return (f"<Workflow("
                # f"id={self.id}, "
                f"created_user_by='{self.created_user_by}', "
                f"updated_user_by='{self.updated_user_by}', "
                f"name={self.name})>"
                )
