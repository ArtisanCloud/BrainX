"""add tenant models

Revision ID: 10000
Revises: None
Create Date: 2024-05-30 21:23:22.807845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app import settings
from app.config.server import ProjectType
from app.models.originaztion.user import table_name_user

from sqlalchemy.dialects.postgresql import UUID
import datetime

# revision identifiers, used by Alembic.
revision: str = '10000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.create_table(
            table_name_user,
            # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
            sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

            sa.Column('tenant_owner_uuid', sa.UUID(), nullable=True, unique=True),
            sa.Column('account', sa.String(), nullable=True),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('nick_name', sa.String(), nullable=True),
            sa.Column('desc', sa.Text(), nullable=True),
            sa.Column('position_id', sa.BigInteger(), nullable=True),
            sa.Column('job_title', sa.String(), nullable=True),
            sa.Column('department_id', sa.BigInteger(), nullable=True),
            sa.Column('mobile_phone', sa.String(), nullable=True),
            sa.Column('gender', sa.String(), nullable=True),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('external_email', sa.String(), nullable=True),
            sa.Column('avatar', sa.String(), nullable=True),
            sa.Column('password', sa.String(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('is_reserved', sa.Boolean(), nullable=True),
            sa.Column('is_activated', sa.Boolean(), nullable=True),
            sa.Column('we_work_user_id', sa.String(), nullable=True),

            sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
            sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
            sa.PrimaryKeyConstraint('uuid'),
            schema="public"
        )


def downgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.drop_table(table_name_user, schema="public")
