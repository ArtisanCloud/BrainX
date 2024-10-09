from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column

from app import settings
from app.models.base import BaseORM


class Group(BaseORM):
    __tablename__ = 'groups'
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    name = mapped_column(String)
    description = mapped_column(String)

    # Polymorphic relationship
    groupable_id = mapped_column(Integer)
    groupable_type = mapped_column(String)

    __mapper_args__ = {
        'polymorphic_on': groupable_type,
        'polymorphic_identity': 'group'
    }

    def __init__(self, name, description, groupable_id, groupable_type):
        super().__init__()
        self.name = name
        self.description = description
        self.groupable_id = groupable_id
        self.groupable_type = groupable_type