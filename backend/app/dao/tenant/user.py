from typing import Tuple, Optional, Union, List

from uuid import uuid4

from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.models.base import BaseStatus
from app.models.originaztion.user import User
from app.models.tenant.tenant import Tenant, TenantDefaultModel


class UserDAO(BaseDAO[User]):
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, User)

    async def load_owner_tenant(self, user: User) -> Tuple[User | None, SQLAlchemyError | None]:
        try:
            stmt = select(Tenant).filter_by(uuid=user.tenant_owner_uuid)
            result = await self.db.execute(stmt)
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
            result = await self.db.execute(stmt)
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
            self.db.add(tenant)

            # create user
            user = User(
                uuid=uuid4(),
                tenant_owner_uuid=tenant.uuid,
                account=user.account,
                name=user.account,
                password=user.password,
                status="active",
            )
            self.db.add(user)

            # connect user and tenant
            # pivot = PivotTenantToUser(
            #     tenant_uuid=tenant.uuid,
            #     user_uuid=user.uuid
            # )
            # pivot.generate_uuid()

            # print(pivot)
            # self.db.add(pivot)

            # create tenant default model
            tenant_default_model_dao = TenantDefaultModelDAO(self.db)
            default_models, exception = await tenant_default_model_dao.get_tenant_default_model_from_config(user)
            if exception:
                return None, exception
            self.db.add_all(default_models)

            # 在这里调用 flush()，以便获取 user 的 uuid
            await self.db.flush()  # 确保所有添加的对象已经持久化到数据库

            await self.db.commit()
            await self.db.refresh(user)

            return user, None

        except SQLAlchemyError as e:

            raise e
