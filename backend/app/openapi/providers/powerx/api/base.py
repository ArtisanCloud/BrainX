from typing import Optional, Dict

from fastapi import APIRouter

from app.openapi.providers.powerx.service.base import PowerXServiceProvider
from app.schemas.base import ResponseSchema

router = APIRouter()


@router.get("/version")
async def api_version() -> Optional[Dict | ResponseSchema]:
    service_power_x = PowerXServiceProvider()
    res, exception = service_power_x.query_get_version()
    if exception is not None:
        return ResponseSchema(
            error=str(exception)
        )
    return res


@router.post("/echo")
async def api_echo() -> Optional[Dict | ResponseSchema]:
    service_power_x = PowerXServiceProvider()
    res, exception = service_power_x.query_echo()
    if exception is not None:
        return ResponseSchema(
            error=exception
        )
    return res
