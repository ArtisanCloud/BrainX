"""add workflow models

Revision ID: 51000
Revises: 14000
Create Date: 2024-06-15 00:45:05.449070

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app import settings
from app.models import Tenant
from app.models.base import table_name_tenant
from app.models.originaztion.user import table_name_user
from app.models.workflow.workflow import table_name_workflow

# revision identifiers, used by Alembic.
revision: str = '51000'
down_revision: Union[str, None] = '14000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_workflow,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_user_by', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('updated_user_by', UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('deleted_by', UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('parent_uuid', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('tag', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.SmallInteger(), nullable=True),
        sa.Column('graph', sa.Text(), nullable=True),
        sa.Column('meta', sa.Text(), nullable=True),

        sa.ForeignKeyConstraint(['tenant_uuid'], [Tenant.__table__.fullname + '.uuid'], ),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),
        schema=settings.database.db_schema
    )


def downgrade() -> None:
    op.drop_table(table_name_workflow, schema=settings.database.db_schema)
