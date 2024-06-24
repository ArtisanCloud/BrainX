from fastapi import Depends, APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger
from app.models.customer import User

from uuid import UUID

router = APIRouter()


@router.get("/")
async def get_customers() -> List[User]:
    """
    Get all documents or documents by their ids
    """
    customers = [User(Id="1", Name="Item 1"), User(Id="2", Name="Item 2")]
    return customers