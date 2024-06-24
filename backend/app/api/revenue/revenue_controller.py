import asyncio

from fastapi import Depends, APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from starlette.requests import Request

from app.api.context_manager import build_request_context
from app.models.revenue import Revenue

from uuid import UUID

router = APIRouter()


@router.get("/", response_model=None)
async def get_revenues(
        # request: Request,
        _=Depends(build_request_context)
) -> List[Revenue]:

    # db = get_db_session()
    # print(db)
    # print(request)
    # await asyncio.sleep(5)

    revenues = [
        Revenue(month='Jan', revenue=2000),
        Revenue(month='Feb', revenue=1800),
        Revenue(month='Mar', revenue=2200),
        Revenue(month='Apr', revenue=2500),
        Revenue(month='May', revenue=2300),
        Revenue(month='Jun', revenue=3200),
        Revenue(month='Jul', revenue=3500),
        Revenue(month='Aug', revenue=3700),
        Revenue(month='Sep', revenue=2500),
        Revenue(month='Oct', revenue=2800),
        Revenue(month='Nov', revenue=3000),
        Revenue(month='Dec', revenue=4800),
    ]
    return revenues
