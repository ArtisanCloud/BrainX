from sqlalchemy import Column, BigInteger, String, Text, DateTime, func, ForeignKey, SmallInteger, UUID
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel, table_name_workflow
from app.models.originaztion.user import table_name_user
from app.models.tenant import table_name_tenant




class Workflow(BaseModel):
    __tablename__ = table_name_workflow

    tenant_uuid = mapped_column('tenant_uuid', String, ForeignKey(table_name_tenant + '.uuid'))
    parent_uuid = mapped_column('parent_uuid', String, ForeignKey(table_name_workflow + '.uuid'))

    name = mapped_column('name', String, nullable=False)
    tag = mapped_column('tag', String, nullable=False)
    description = mapped_column('description', Text)
    type = mapped_column('type', SmallInteger)
    graph = mapped_column('graph', Text)  # Using Text for JSON data
    meta = mapped_column('meta', Text)  # Using Text for JSON data

    created_by = mapped_column('created_by', UUID, nullable=True, index=True)
    updated_by = mapped_column('updated_by', UUID, nullable=True, index=True)
    deleted_by = mapped_column('deleted_by', UUID, nullable=True, index=True)

    def __repr__(self):
        return f"<Workflow(id={self.id}, name={self.name})>"
