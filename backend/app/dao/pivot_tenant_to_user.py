from typing import List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.models.tenant import PivotTenantToUser


class PivotTenantToUserDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pivot(self, tenant_uuid: str, user_uuid: str) -> Tuple[PivotTenantToUser | None, Exception | None]:
        try:
            pivot = PivotTenantToUser(tenant_uuid=tenant_uuid, user_uuid=user_uuid)
            self.db.add(pivot)
            await self.db.commit()
            return pivot, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def delete_pivot(self, tenant_uuid: str, user_uuid: str) -> Tuple[bool, Exception | None]:
        try:
            stmt = select(PivotTenantToUser).filter_by(tenant_uuid=tenant_uuid, user_uuid=user_uuid)
            result = await self.db.execute(stmt)
            pivot = result.scalar_one_or_none()

            if pivot:
                self.db.delete(pivot)
                await self.db.commit()
                return True, None
            else:
                return False, Exception(
                    f"Pivot record with tenant_uuid={tenant_uuid} and user_uuid={user_uuid} not found")
        except SQLAlchemyError as e:
            await self.db.rollback()
            return False, e
