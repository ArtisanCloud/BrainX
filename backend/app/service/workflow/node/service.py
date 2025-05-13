from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.workflow.workflow import WorkflowDAO


class WorkflowService:
    def __init__(self,async_db: AsyncSession):
        self.app_dao = WorkflowDAO(async_db)

