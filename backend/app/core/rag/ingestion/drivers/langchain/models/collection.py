from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

from app import settings
from app.models.base import BaseORM

table_name_langchain_pg_collection = "langchain_pg_collection"


class LangchainPGCollection(BaseORM):
    __tablename__ = table_name_langchain_pg_collection
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    # 表字段定义
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    cmetadata = Column(JSON, nullable=True)

    def __repr__(self):
        return (f"<LangchainPGCollection(uuid={self.uuid}, "
                f"name='{self.name}', "
                f"cmetadata={self.cmetadata})>")
