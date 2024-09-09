from abc import ABC, abstractmethod
from typing import Any

import httpx


class ServiceProvider(ABC):
    token = None

    @abstractmethod
    def auth(self):
        pass

    @abstractmethod
    def get_access_token(self):
        pass

    def http_get(self, url: str, params: Any = None, use_auth: bool = True, headers: dict = None):
        try:
            headers = headers or {}  # 使用空字典作为默认值
            if use_auth:
                access_token = self.get_access_token()
                headers["Authorization"] = f"Bearer {access_token}"

            with httpx.Client() as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()  # 确保请求成功

            return response.json()  # 返回 JSON 响应数据
        except httpx.HTTPStatusError as http_err:
            # 处理 HTTP 错误
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as e:
            # 处理其他错误
            raise Exception(f"An error occurred: {e}")

    def http_post(self, url: str, json: Any = None, use_auth: bool = True, headers: dict = None):
        try:
            headers = headers or {}  # 使用空字典作为默认值
            if use_auth:
                access_token = self.get_access_token()
                headers["Authorization"] = f"Bearer {access_token}"

            with httpx.Client() as client:
                response = client.post(url, json=json, headers=headers)
                response.raise_for_status()  # 确保请求成功

            return response.json()  # 返回 JSON 响应数据

        except httpx.HTTPStatusError as http_err:
            # 处理 HTTP 错误
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as e:
            # 处理其他错误
            raise Exception(f"An error occurred: {e}")
