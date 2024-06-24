"""add workflow model

Revision ID: 000000000010
Revises: caa5b72ec88a
Create Date: 2024-06-15 00:45:05.449070

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.originaztion.user import table_name_user
from app.models.workflow import table_name_workflow

# revision identifiers, used by Alembic.
revision: str = '000000000010'
down_revision: Union[str, None] = '000000000004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_workflow,
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True),  index=True, unique=True),

        sa.Column('tenant_uuid', sa.UUID(), nullable=True),
        sa.Column('parent_uuid', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('tag', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.SmallInteger(), nullable=True),
        sa.Column('graph', sa.Text(), nullable=True),
        sa.Column('meta', sa.Text(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True, index=True),
        sa.Column('updated_by', sa.String(), nullable=True, index=True),
        sa.Column('deleted_by', sa.String(), nullable=True, index=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.ForeignKeyConstraint(['tenant_uuid'], [table_name_user + '.uuid'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table(table_name_workflow)
