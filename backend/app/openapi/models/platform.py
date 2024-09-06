from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from app.models.base import BaseORM, table_name_platform


class Platform(BaseORM):
    __tablename__ = table_name_platform

    name = mapped_column(String)
    access_key = mapped_column(String)
    secret_key = mapped_column(String)
