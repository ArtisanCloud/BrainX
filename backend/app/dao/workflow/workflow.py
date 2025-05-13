from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.models.workflow.workflow import Workflow


class WorkflowDAO(BaseDAO[Workflow]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(Workflow, async_db, sync_db)
