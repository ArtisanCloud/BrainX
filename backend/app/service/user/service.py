from typing import Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.tenant.user import UserDAO
from app.models.originaztion.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_dao = UserDAO(db)

    async def check_register_account_exist(self, account: str) -> Tuple[bool | None, Exception | None]:

        try:
            user, exception = await self.user_dao.get_by_account(account)
            if exception is not None:
                return None, exception

            return user, None
        except SQLAlchemyError as e:
            return None, e

    async def init_user(self, user: User) -> Tuple[User | None, Exception | None]:
        user, exception = await self.user_dao.init_user(user)

        return user, exception
