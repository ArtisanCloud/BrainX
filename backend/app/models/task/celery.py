
from sqlalchemy import Column, String, Text, Enum, DateTime, Integer
from sqlalchemy.orm import declarative_base
from enum import Enum as PyEnum
import datetime

from app import settings

Base = declarative_base()

class TaskStatus(PyEnum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"
    REVOKED = "revoked"

class CeleryTask(Base):
    __tablename__ = 'celery_tasks'
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), unique=True, index=True)
    name = Column(String(255), index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return (f"<CeleryTask("
                # f"id={self.id}, "
                f"task_id={self.task_id}, name={self.name}, status={self.status})>")
