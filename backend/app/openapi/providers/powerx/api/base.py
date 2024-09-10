# powerx/interface.py
from fastapi import APIRouter, Depends

import requests

from app import settings
from app.openapi.providers.powerx.provider_auth.authenticate import verify_token

router = APIRouter()

# PowerX 的 OpenAPI 基础 URL
POWERX_BASE_URL = settings.openapi.provider.power_x.base_url


@router.get("/version", tags=["PowerX"])
async def get_version(token: str = Depends(verify_token)):
    """获取 PowerX 的版本信息"""
    response = requests.get(f"{POWERX_BASE_URL}/version", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch version"}


@router.get("/echo", tags=["PowerX"])
async def echo(message: str, token: str = Depends(verify_token)):
    """将传入的信息返回"""
    response = requests.get(f"{POWERX_BASE_URL}/echo", params={"message": message},
                            headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to echo message"}
