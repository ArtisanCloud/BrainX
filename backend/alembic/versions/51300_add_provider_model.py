"""add models providers  models

Revision ID: 51300
Revises: 51200
Create Date: 2024-06-15 15:42:58.360088

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app import settings
from app.models.base import table_name_provider_model

# revision identifiers, used by Alembic.
revision: str = '51300'
down_revision: Union[str, None] = '51200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_provider_model,  # 使用表名
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('provider_uuid', UUID(as_uuid=True), nullable=False, index=False),
        sa.Column('provider_name', sa.String, nullable=False),
        sa.Column('model_name', sa.String, nullable=False),
        sa.Column('model_type', sa.String, nullable=False),
        sa.Column('encrypted_config', sa.Text, nullable=True),
        sa.Column('is_valid', sa.Boolean, nullable=False),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),
        schema=settings.database.db_schema

    )


def downgrade() -> None:
    op.drop_table(table_name_provider_model, schema=settings.database.db_schema)
