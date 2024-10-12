"""Add Data Image Embedding model

Revision ID: 52000
Revises: 51700
Create Date: 2024-10-09 21:26:10.804534

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import Text

from app import settings
from app.models.base import table_name_data_image_embedding
from sqlalchemy.dialects.postgresql import UUID, BYTEA, VARCHAR

# revision identifiers, used by Alembic.
revision: str = '52000'
down_revision: Union[str, None] = '51700'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_data_image_embedding,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', VARCHAR(36), nullable=False, comment='集合ID', index=True, unique=True),

        # collection_id 字段
        sa.Column('collection_id', VARCHAR(36), nullable=False, comment='集合ID'),

        # question 字段
        sa.Column('question', VARCHAR(800), comment='问题'),

        # image 字段
        sa.Column('image', BYTEA, comment='存储二进制数据'),

        # embedding 字段
        sa.Column('embedding', Vector(768), comment='768维的向量'),

        sa.Column('c_metadata', Text, comment='metadata'),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),
        schema=settings.database.db_schema
    )


def downgrade() -> None:
    op.drop_table(table_name_data_image_embedding, schema=settings.database.db_schema)
