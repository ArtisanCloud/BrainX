from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.workflow.workflow import WorkflowDAO


class WorkflowService:
    def __init__(self, db: AsyncSession):
        self.app_dao = WorkflowDAO(db)

