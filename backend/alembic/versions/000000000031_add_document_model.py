"""Add Document model

Revision ID: 000000000031
Revises: 000000000030
Create Date: 2024-07-15 21:29:16.538231

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import table_name_document, table_name_tenant, table_name_user, table_name_dataset

# revision identifiers, used by Alembic.
revision: str = '000000000031'
down_revision: Union[str, None] = '000000000030'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_document,
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('dataset_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_user_by', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('updated_user_by', UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('resource_uuid', UUID(as_uuid=True), nullable=True, index=True),

        sa.Column('title', sa.String(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('type', sa.SmallInteger(), nullable=True),
        sa.Column('document_index', sa.Integer(), nullable=True),
        sa.Column('batch_index', sa.Integer(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('resource_url', sa.String(), nullable=True),

        sa.Column('process_start_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('process_end_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('parse_start_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('parse_end_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('split_start_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('split_end_at', sa.TIMESTAMP(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(['tenant_uuid'], [table_name_tenant + '.uuid'], ),
        sa.ForeignKeyConstraint(['dataset_uuid'], [table_name_dataset + '.uuid'], ),
        sa.ForeignKeyConstraint(['created_user_by'], [table_name_user + '.uuid'], ),
        sa.ForeignKeyConstraint(['updated_user_by'], [table_name_user + '.uuid'], ),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table(table_name_document)
