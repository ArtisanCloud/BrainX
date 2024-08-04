import hashlib
import uuid
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.models.tenant.pivot_tenant_to_user import PivotTenantToUser


class PivotTenantToUserDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_uuid(self):
        str_merged_uuid = self.user_uuid + self.tenant_uuid

        # 使用 SHA-256 哈希函数计算合并后的字符串的摘要
        hash_object = hashlib.sha256()
        hash_object.update(str_merged_uuid.encode())
        hash_digest = hash_object.digest()

        # 取摘要的前16字节作为UUID的字节序列
        uuid_bytes = hash_digest[:16]

        # 将哈希摘要转换为 UUID
        generated_uuid = uuid.UUID(bytes=uuid_bytes)

        return generated_uuid

    async def create_pivot(self, tenant_uuid: str, user_uuid: str) -> Tuple[PivotTenantToUser | None, SQLAlchemyError | None]:
        try:
            pivot = PivotTenantToUser(tenant_uuid=tenant_uuid, user_uuid=user_uuid)
            self.db.add(pivot)

            return pivot, None
        except SQLAlchemyError as e:

            return None, e

    async def delete_pivot(self, tenant_uuid: str, user_uuid: str) -> Tuple[bool, SQLAlchemyError | None]:
        try:
            stmt = select(PivotTenantToUser).filter_by(tenant_uuid=tenant_uuid, user_uuid=user_uuid)
            result = await self.db.execute(stmt)
            pivot = result.scalar_one_or_none()

            if pivot:
                self.db.delete(pivot)

                return True, None
            else:
                return False, Exception(
                    f"Pivot record with tenant_uuid={tenant_uuid} and user_uuid={user_uuid} not found")
        except SQLAlchemyError as e:

            return False, e
