from fastapi import Depends, APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.models.invoice import Invoice

from uuid import UUID

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def get_invoices() -> List[Invoice]:
    """
    获取所有发票
    """
    # 模拟一些客户数据
    customers = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6},
        {"id": 7},
        {"id": 8},
    ]

    # 生成发票列表
    invoices = [
        Invoice(
            customer_id=customers[0]["id"],
            amount=15795,
            status='pending',
            date='2022-12-06',
            name="John Doe",
            email="test@test.com",
            image_url='/customers/delba-de-oliveira.png',
        ),
        Invoice(
            customer_id=customers[1]["id"],
            amount=20348,
            status='pending',
            date='2022-11-14',
            name="John Doe",
            email="test@test.com",
            image_url='/customers/delba-de-oliveira.png',
        ),
        Invoice(
            customer_id=customers[4]["id"],
            amount=3040,
            status='paid',
            date='2022-10-29',
            name="John Doe",
            email="test@test.com",
            image_url='/customers/delba-de-oliveira.png',
        ),
        # 省略其他发票数据...
    ]

    return invoices
