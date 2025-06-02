from typing import Tuple, Optional, Union, List

from uuid import uuid4

from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.database.session_manager import is_manual_session
from app.models.base import BaseStatus
from app.models.originaztion.user import User
from app.models.tenant.tenant import Tenant, TenantDefaultModel


class UserDAO(BaseDAO[User]):
    def __init__(self, async_db: AsyncSession = None, sync_db: Session = None):
        super().__init__(User, async_db, sync_db)

    async def load_owner_tenant(self, user: User) -> Tuple[User | None, SQLAlchemyError | None]:
        try:
            stmt = select(Tenant).filter_by(uuid=user.tenant_owner_uuid)
            result = await self.async_db.execute(stmt)
            user.owned_tenant = result.scalar_one_or_none()

        except SQLAlchemyError as e:
            return None, e

        return user, None

    async def get_by_account(self, account: str) -> Tuple[Optional[User], Optional[Exception]]:
        """
        根据 Account 获取模型对象
        """

        try:
            stmt = select(User).filter(User.account == account)
            result = await self.async_db.execute(stmt)
            return result.scalar_one_or_none(), None

        except SQLAlchemyError as e:
            return None, e

    async def init_user(self, user: User) -> Tuple[User | None, Optional[Exception]]:
        try:
            # create tenant
            tenant = Tenant(
                uuid=uuid4(),
                name=f"{user.account}的租户",
                status=BaseStatus.ACTIVE,
            )
            self.async_db.add(tenant)

            # create user
            user = User(
                uuid=uuid4(),
                tenant_owner_uuid=tenant.uuid,
                account=user.account,
                name=user.account,
                password=user.password,
                status="active",
            )
            self.async_db.add(user)

            # connect user and tenant
            # pivot = PivotTenantToUser(
            #     tenant_uuid=tenant.uuid,
            #     user_uuid=user.uuid
            # )
            # pivot.generate_uuid()

            # print(pivot)
            # self.async_db.add(pivot)

            # create tenant default model
            tenant_default_model_dao = TenantDefaultModelDAO(self.async_db)
            default_models, exception = await tenant_default_model_dao.get_tenant_default_model_from_config(user)
            if exception:
                return None, exception
            self.async_db.add_all(default_models)

            # 在这里调用 flush()，以便获取 user 的 uuid
            await self.async_db.flush()  # 确保所有添加的对象已经持久化到数据库

            if not is_manual_session(self.async_db):
                await self.async_db.commit()
            await self.async_db.refresh(user)

            return user, None

        except SQLAlchemyError as e:
            if not is_manual_session(self.async_db):
                await self.async_db.rollback()
            raise e
