from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel, table_name_image_embedding
from sqlalchemy import Column, String, Text, BINARY
from pgvector.sqlalchemy import Vector

table_name_text_embedding = 'data_embeddings'


# class Document(BaseModel):
#     __tablename__ = table_name_text_embedding
#
#     name = mapped_column('name', String)
#     text = mapped_column('text', Text)
#     node_id = mapped_column('node_id', String)
#
#
# class ImageDocument(BaseModel):
#     __tablename__ = table_name_image_embedding
#
#     name = mapped_column('name', String)
#     doc_id = mapped_column('doc_id', String)
#     question = mapped_column('question', String)
#     image = mapped_column('image', BINARY)
#     embedding = mapped_column('embedding', Vector(768))
