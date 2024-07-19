from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core.libs.security import check_password
from app.models.originaztion.user import User
from app.schemas.auth import ResponseLoginUser, AccessTokenSchema, ALGORITHM, auth_user_uuid_key, auth_tenant_uuid_key
from app.service.user.service import UserService
from jose import JWTError, jwt


def sign_token(user: User, secret_key, expires_in) -> AccessTokenSchema:
    now = datetime.now(timezone.utc)
    access_token_payload = {
        auth_tenant_uuid_key: str(user.tenant_owner_uuid),
        auth_user_uuid_key: str(user.uuid),
        'name': user.name,
        'exp': now + timedelta(seconds=expires_in)
    }
    access_token = jwt.encode(access_token_payload, secret_key, algorithm=ALGORITHM)

    refresh_token_payload = {
        'sub': str(user.uuid),
        'exp': now + timedelta(seconds=(30 * 24 * 3600 + expires_in))
    }
    refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm=ALGORITHM)

    return AccessTokenSchema(token_type="Bearer", access_token=access_token, refresh_token=refresh_token,
                             expires_in=expires_in)


async def login_by_account(
        db: AsyncSession,
        account: str, password: str
) -> tuple[AccessTokenSchema | None, Exception | None]:
    service_user = UserService(db)

    # check user exist or not
    user, exception = await service_user.user_dao.get_by_account(account)
    if exception is not None:
        return None, exception

    if user is None:
        return None, Exception("user not exist")

    # check password
    try:
        passed = check_password(user.password, password)
    except Exception as e:
        return None, e
    # print(f"passed:{passed}")
    if not passed:
        return None, Exception("password error")

    # load user owned tenant
    # user, exception = service_user.user_dao.load_owner_tenant(user)
    # if exception is not None:
    #     return None, exception
    if user.tenant_owner_uuid == "":
        return None, Exception("user has not bind owned tenant")

    # create token
    access_token = sign_token(user, settings.jwt.jwt_secret, settings.jwt.expire_in)
    # print(access_token)

    return access_token, exception
