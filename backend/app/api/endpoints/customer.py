from fastapi import Depends, APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.schema.customer import Customer

from uuid import UUID

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def get_customers() -> List[Customer]:
    """
    Get all documents or documents by their ids
    """
    customers = [Customer(Id="1", Name="Item 1"), Customer(Id="2", Name="Item 2")]
    return customers