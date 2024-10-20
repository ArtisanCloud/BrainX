"""Add MediaResource models

Revision ID: 60000
Revises: 52000
Create Date: 2024-05-12 22:46:49.340958

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app import settings
from app.config.server import ProjectType
from app.models.media_resource.model import table_name_media_resource
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '60000'
down_revision: Union[str, None] = '52000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.create_table(
            table_name_media_resource,
            # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
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
            sa.PrimaryKeyConstraint('uuid'),
            schema='public'
        )


def downgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.drop_table(table_name_media_resource, schema='public')
