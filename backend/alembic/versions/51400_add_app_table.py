"""add app models

Revision ID: 51400
Revises: 51300
Create Date: 2024-04-22 15:10:57.595552

"""
import datetime
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import sqlalchemy as sa

from app import settings
from app.models.app.app import table_name_app
from app.models.originaztion.user import table_name_user, User
from app.models.tenant.tenant import table_name_tenant, Tenant
from app.models.workflow.workflow import table_name_workflow, Workflow

# revision identifiers, used by Alembic.
revision: str = '51400'
down_revision: Union[str, None] = '51300'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_app,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', sa.UUID(), nullable=True, index=True),
        sa.Column('created_user_by', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('updated_user_by', UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('app_model_config_uuid', sa.UUID(), nullable=True, index=True),
        sa.Column('workflow_uuid', sa.UUID(), nullable=True, index=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('type', sa.SmallInteger(), nullable=True),
        sa.Column('mode', sa.SmallInteger(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('persona', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),

        sa.ForeignKeyConstraint(['tenant_uuid'], [Tenant.__table__.fullname + '.uuid'], ),
        sa.ForeignKeyConstraint(['created_user_by'], [User.__table__.fullname + '.uuid'], ),
        sa.ForeignKeyConstraint(['workflow_uuid'], [Workflow.__table__.fullname + '.uuid'], ),
        sa.PrimaryKeyConstraint('uuid'),
        schema=settings.database.db_schema
    )


def downgrade() -> None:
    op.drop_table(table_name_app, schema=settings.database.db_schema)
