"""add models providers  models

Revision ID: 000000000012
Revises: 000000000020
Create Date: 2024-06-15 15:42:58.360088

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.model_provider.model_provider import table_name_model_provider

# revision identifiers, used by Alembic.
revision: str = '000000000012'
down_revision: Union[str, None] = '000000000010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_model_provider,  # 使用表名
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('model_name', sa.String, nullable=False),
        sa.Column('model_type', sa.String, nullable=False),
        sa.Column('encrypted_config', sa.Text, nullable=True),
        sa.Column('is_valid', sa.Boolean, nullable=False),
        sa.Column('last_used', sa.TIMESTAMP(timezone=True), nullable=True),

        sa.Column('quota_type', sa.SmallInteger, nullable=True),
        sa.Column('quota_limit', sa.BigInteger, nullable=True),
        sa.Column('quota_used', sa.BigInteger, default=0, nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid')


    )



def downgrade() -> None:
    op.drop_table(table_name_model_provider)
