from typing import Tuple, Any

from app import settings
from app.cache.factory import CacheFactory
from app.openapi.providers.powerx.schemas.auth import ResponseAuthToken
from app.openapi.providers.service_provider import ServiceProvider
from app.openapi.schemas.apqp.opl import ResponsePaginationOPL

# PowerX 的 OpenAPI 基础 URL
POWERX_BASE_URL = settings.openapi.providers.power_x.base_url


class PowerXServiceProvider(ServiceProvider):
    def __init__(self, base_url: str = POWERX_BASE_URL):
        self.base_url = base_url
        self.token: ResponseAuthToken | None = None
        self.token_key = "provider.powerx.access_token"
        self.cache = CacheFactory.initialize_cache(settings.cache.driver)
        self.cache.connect()

    def __del__(self):
        # 在对象被销毁时释放 Redis 连接
        if self.cache:
            self.cache.disconnect()

    def auth(self) -> Tuple[ResponseAuthToken | None, Exception | None]:
        try:
            url = f"{self.base_url}/auth"
            body = {
                "accessKey": settings.openapi.providers.power_x.access_key,
                "secretKey": settings.openapi.providers.power_x.secret_key,
            }

            res = self.http_post(url, json=body, use_auth=False)

            # 将 JSON 数据转换为 ResponseAuthToken 对象
            token = ResponseAuthToken(**res)
            return token, None

        except Exception as e:
            return None, e

    def get_access_token(self):
        token = self.cache.get(self.token_key)
        if token is None:
            self.token, exception = self.auth()

            if exception is not None:
                raise Exception(f"request powerx provider auth error: {exception}")

            expired_in = self.token.expiresIn
            self.cache.set(self.token_key, self.token, expire=expired_in)

        elif isinstance(token, dict):
            self.token = ResponseAuthToken(**token)

        return self.token.accessToken

    def query_get_version(self) -> Tuple[Any | None, Exception | None]:
        """获取 PowerX 的版本信息"""
        url = f"{self.base_url}/version"
        try:
            res = self.http_get(url)
            return res, None
        except Exception as e:
            return None, e

    def query_echo(self) -> Tuple[Any | None, Exception | None]:
        """将传入的信息返回"""
        url = f"{self.base_url}/echo"
        body = {
            "message": "hello"
        }

        try:
            res = self.http_post(url, json=body)
            return res, None
        except Exception as e:
            return None, e

    def query_opl_data(
            self,
            page: int, page_count: int,
            order_by: str = 'desc',
    ) -> Tuple[ResponsePaginationOPL | None, Exception | None]:
        url = f"{self.base_url}/aqpq/question-answer/opl/page-list"
        params = {
            "pageIndex": page,
            "pageSize": page_count,
            "orderBy": order_by,
        }
        try:
            res = self.http_get(url, params=params)

            # 将 JSON 数据转换为 ResponsePaginationOPL 对象
            response_pagination_opl = ResponsePaginationOPL(**res)
            return response_pagination_opl, None

        except Exception as e:
            return None, e
