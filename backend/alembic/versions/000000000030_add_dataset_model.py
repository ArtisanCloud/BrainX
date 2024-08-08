"""Add Dataset models

Revision ID: 000000000030
Revises: 000000000020
Create Date: 2024-07-15 21:29:10.358912

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.base import table_name_dataset, table_name_tenant, table_name_user, table_name_dataset_segment_rule

# revision identifiers, used by Alembic.
revision: str = '000000000030'
down_revision: Union[str, None] = '000000000020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_dataset_table() -> None:
    op.create_table(
        table_name_dataset,
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_user_by', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('updated_user_by', UUID(as_uuid=True), nullable=True, index=True),

        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('dataset_format', sa.SmallInteger(), nullable=True),
        sa.Column('import_type', sa.SmallInteger(), nullable=True),
        sa.Column('driver_type', sa.SmallInteger(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('embedding_model', sa.String(255), nullable=True),
        sa.Column('embedding_model_provider', sa.String(255), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),

        sa.ForeignKeyConstraint(['tenant_uuid'], [table_name_tenant + '.uuid'], ),
        sa.ForeignKeyConstraint(['created_user_by'], [table_name_user + '.uuid'], ),
        sa.ForeignKeyConstraint(['updated_user_by'], [table_name_user + '.uuid'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def create_dataset_segment_rule_table() -> None:
    op.create_table(
        table_name_dataset_segment_rule,
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('dataset_uuid', UUID(as_uuid=True), nullable=False),

        sa.Column('mode', sa.SmallInteger(), nullable=True),
        sa.Column('rules', sa.Text(), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),

        sa.ForeignKeyConstraint(['dataset_uuid'], [table_name_dataset + '.uuid'], ),

        sa.PrimaryKeyConstraint('id'),
    )


def upgrade() -> None:
    create_dataset_table()
    create_dataset_segment_rule_table()


def downgrade() -> None:
    op.drop_table(table_name_dataset_segment_rule)
    op.drop_table(table_name_dataset)
