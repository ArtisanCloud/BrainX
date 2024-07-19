from sqlalchemy.ext.asyncio import AsyncSession

from app.core.libs.security import hash_password
from app.models.originaztion.user import User
from app.schemas.tenant.user import UserSchema
from app.service.user.service import UserService


def transform_user_to_reply(user: User) -> [UserSchema | None]:
    if user is None:
        return None

    return UserSchema.from_orm(user)


async def create_user_by_account(
        db: AsyncSession,
        account: str, password: str
):
    service_user = UserService(db)

    # check user exist or not
    exist, exception = await service_user.check_register_account_exist(account)
    if exception is not None:
        return None, exception

    if exist:
        return None, Exception("user already exist")

    # hash password
    hashed_password = hash_password(password)
    # upsert 客户
    user = User(
        account=account,
        password=hashed_password
    )
    user, exception = await service_user.init_user(user)

    if exception is not None:
        return None, exception

    return transform_user_to_reply(user), None
