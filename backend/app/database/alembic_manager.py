# Import all the models, so that Base has them before being
# imported by Alembic
from alembic import command
from alembic.config import Config

from app.config.config import settings
from app.models.base import Base  # noqa


class AlembicManager:
    def __init__(self):
        # Change DB URL to use psycopg driver for this specific check
        self.db_url = settings.database.url.replace(
            "postgresql+asyncpg://", "postgresql+psycopg://"
        )
        # Set up Alembic configuration
        self.alembic_cfg = Config("alembic.ini")
        self.alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)

    def upgrade(self):
        try:
            # Perform database upgrade
            print(self.alembic_cfg)
            command.upgrade(self.alembic_cfg, "head")
            return None
        except Exception as e:
            return e

    def downgrade(self, steps: int = 1):
        try:
            # Perform database downgrade by steps
            command.downgrade(self.alembic_cfg, f"-{steps}")
            return None
        except Exception as e:
            return e

    def downgrade_all(self):
        try:
            # Perform database downgrade to base version
            command.downgrade(self.alembic_cfg, "base")
            return None
        except Exception as e:
            return e

    def downgrade_to_version(self, version: str):
        try:
            # Perform database downgrade to specific version
            command.downgrade(self.alembic_cfg, version)
            return None
        except Exception as e:
            return e

    def upgrade_to_version(self, version: str):
        try:
            # Perform database upgrade to specific version
            command.upgrade(self.alembic_cfg, version)
            return None
        except Exception as e:
            return e

# async def perform_database_upgrade() -> Exception | None:
#     try:
#         # Change DB URL to use psycopg driver for this specific check
#         db_url = settings.database.url.replace(
#             "postgresql+asyncpg://", "postgresql+psycopg://"
#         )
#
#         # Set up Alembic configuration
#         alembic_cfg = Config("alembic.ini")
#         alembic_cfg.set_main_option("sqlalchemy.url", db_url)
#
#         # Perform database upgrade
#         command.upgrade(alembic_cfg, "head")
#
#         return None
#
#     except Exception as e:
#         return e
