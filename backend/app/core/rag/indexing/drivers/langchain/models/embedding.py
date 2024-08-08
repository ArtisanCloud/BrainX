from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel

table_name_langchain_pg_embedding = "langchain_pg_embedding"


class LangchainPGEmbedding(BaseModel):
    __tablename__ = table_name_langchain_pg_embedding

    # 表字段定义
    id = Column(String, primary_key=True, unique=True, nullable=False)
    collection_id = Column(UUID(as_uuid=True), nullable=True)
    embedding = Column(Vector, nullable=True)  # 使用 sqlalchemy_pgvector 库中的 PGVector 类型
    document = Column(String, nullable=True)
    cmetadata = Column(JSONB, nullable=True)

    def __repr__(self):
        return (f"<LangchainPGEmbedding(id='{self.id}',"
                f" collection_id={self.collection_id}, "
                f"embedding={self.embedding}, "
                f"document='{self.document}', "
                f"cmetadata={self.cmetadata})>")
