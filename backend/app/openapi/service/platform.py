from sqlalchemy.ext.asyncio import AsyncSession

from app.openapi.dao.platform import PlatformDAO
from app.schemas.auth import AccessTokenSchema


class PlatformService:
    def __init__(self, db: AsyncSession):
        self.platform_dao = PlatformDAO(db)

    async def auth_by_account(self,
            db: AsyncSession,
            access_key: str, secret_key: str
    ) -> tuple[AccessTokenSchema | None, Exception | None]:

        # # check platform exist or not
        # platform, exception = await self.platform_dao.async_get_by_access_key(account)
        # if exception is not None:
        #     return None, exception
        #
        # if platform is None:
        #     return None, Exception("platform not exist")
        #
        # # check password
        # try:
        #     passed = check_password(platform.password, password)
        # except Exception as e:
        #     return None, e
        # # print(f"passed:{passed}")
        # if not passed:
        #     return None, Exception("password error")

        # create token
        # access_token = sign_token(platform, settings.jwt.jwt_secret, settings.jwt.expire_in)
        # print(access_token)

        # return access_token, exception

        return None, None

