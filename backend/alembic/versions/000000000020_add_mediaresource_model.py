"""Add MediaResource models

Revision ID: 000000000020
Revises: 6668cc8afeca
Create Date: 2024-05-12 22:46:49.340958

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models.media_resource.model import table_name_media_resource
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '000000000020'
down_revision: Union[str, None] = '000000000016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_media_resource,
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_user_by', UUID(as_uuid=True), nullable=False, index=True),

        sa.Column('filename', sa.String(), comment='名称'),
        sa.Column('size', sa.Integer(), comment='尺寸'),
        sa.Column('width', sa.Integer(), comment='宽度'),
        sa.Column('height', sa.Integer(), comment='长度'),
        sa.Column('url', sa.String(), comment='url'),
        sa.Column('bucket_name', sa.String(), comment='Bucket名称'),
        sa.Column('is_local_stored', sa.Boolean(), comment='是否本地存储', default=False),
        sa.Column('content_type', sa.String(), comment='内容类型'),
        sa.Column('resource_type', sa.String(), comment='媒体类型'),
        sa.Column('sort_index', sa.Integer(), comment='排序索引'),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table(table_name_media_resource)
