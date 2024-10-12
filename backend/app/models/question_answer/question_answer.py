from sqlalchemy.dialects.postgresql import BYTEA , TSVECTOR
from sqlalchemy.orm import mapped_column

from app import settings
from app.models.base import BaseORM,  table_name_data_image_embedding
from sqlalchemy import Integer, VARCHAR, Text
from pgvector.sqlalchemy import Vector


# class Document(BaseORM):
#     __tablename__ = table_name_text_embedding
#
#     name = mapped_column('name', String)
#     text = mapped_column('text', Text)
#     node_id = mapped_column('node_id', String)
#
#
# class ImageDocument(BaseORM):
#     __tablename__ = table_name_image_embedding
#
#     name = mapped_column('name', String)
#     doc_id = mapped_column('doc_id', String)
#     question = mapped_column('question', String)
#     image = mapped_column('image', BINARY)
#     embedding = mapped_column('embedding', Vector(768))


class DataImageEmbedding(BaseORM):
    __tablename__ = table_name_data_image_embedding  # 表名
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    doc_id = mapped_column(VARCHAR(36), nullable=False)  # VARCHAR(36), not null
    question = mapped_column(VARCHAR(800))  # varchar(800)
    image = mapped_column(BYTEA)  # bytea, 存储二进制数据
    embedding = mapped_column(Vector(768))  # vector(768)
    c_metadata = mapped_column(Text)  # meta text
