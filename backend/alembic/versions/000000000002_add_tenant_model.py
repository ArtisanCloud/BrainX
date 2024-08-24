"""add tenant models

Revision ID: 000000000002
Revises: 70a699b5a5b5
Create Date: 2024-06-15 00:44:38.755516

"""
import datetime
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import sqlalchemy as sa

from app.models.tenant.tenant import table_name_tenant

# revision identifiers, used by Alembic.
revision: str = '000000000002'
down_revision: Union[str, None] = '000000000001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_tenant,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('plan', sa.SmallInteger()),
        sa.Column('status', sa.SmallInteger()),
        sa.Column('encrypted_public_key', sa.Text()),
        sa.Column('config', sa.Text()),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table(table_name_tenant)
