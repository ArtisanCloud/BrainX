"""Add Document models

Revision ID: 72000
Revises: 71000
Create Date: 2024-07-15 21:29:16.538231

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import table_name_document, table_name_tenant, table_name_user, table_name_dataset, \
    table_name_media_resource, table_name_dataset_segment_rule

# revision identifiers, used by Alembic.
revision: str = '72000'
down_revision: Union[str, None] = '71000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_document,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), sa.ForeignKey(table_name_tenant + '.uuid'), nullable=False,
                  index=True),
        sa.Column('dataset_uuid', UUID(as_uuid=True), sa.ForeignKey(table_name_dataset + '.uuid'), nullable=False,
                  index=True),

        # Resource info
        sa.Column('data_source_type', sa.SmallInteger(), nullable=False),
        sa.Column('resource_uuid', UUID(as_uuid=True), sa.ForeignKey(table_name_media_resource + '.uuid'),
                  nullable=True, index=True),
        sa.Column('resource_url', sa.String(), nullable=False),

        # Document status
        sa.Column('status', sa.SmallInteger(), nullable=False),
        sa.Column('type', sa.SmallInteger(), nullable=False),
        sa.Column('content_type', sa.SmallInteger(), nullable=False),

        sa.Column('batch', sa.String(), nullable=True),
        sa.Column('dataset_process_rule_uuid', UUID(as_uuid=True),
                  sa.ForeignKey(table_name_dataset_segment_rule + '.uuid'), nullable=True),

        sa.Column('created_source', sa.String(), nullable=True),
        sa.Column('created_user_by', UUID(as_uuid=True), sa.ForeignKey(table_name_user + '.uuid'), nullable=False,
                  index=True),
        sa.Column('updated_user_by', UUID(as_uuid=True), sa.ForeignKey(table_name_user + '.uuid'), nullable=True,
                  index=True),

        # Step flow
        sa.Column('indexing_status', sa.SmallInteger(), nullable=False),
        sa.Column('process_start_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('process_end_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Step parsing
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('parse_start_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Step cleaning
        sa.Column('clean_start_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Step splitting
        sa.Column('split_start_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Step indexing with embedding and vector store
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('indexing_latency', sa.Float(), nullable=True),


        # Pause
        sa.Column('is_paused', sa.Boolean(), nullable=False, default=False),
        sa.Column('paused_by', UUID(as_uuid=True), sa.ForeignKey(table_name_user + '.uuid'), nullable=True, index=True),
        sa.Column('paused_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Error
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('error_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Archive
        sa.Column('is_archived', sa.Boolean(), nullable=True, default=False),
        sa.Column('archived_reason', sa.String(), nullable=True),
        sa.Column('archived_by', UUID(as_uuid=True), sa.ForeignKey(table_name_user + '.uuid'), nullable=True,
                  index=True),
        sa.Column('archived_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Document info
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('document_type', sa.String(50), nullable=True),
        sa.Column('document_meta', sa.JSON(), nullable=True),
        sa.Column('document_index', sa.Integer(), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table(table_name_document)
