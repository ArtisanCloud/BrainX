from fastapi import APIRouter
import logging
from app.models.originaztion.user import User

from app.schemas.customer import ResponseUserList

router = APIRouter()


@router.get("/")
async def api_get_customers() -> ResponseUserList:
    """
    Get all documents or documents by their ids
    """
    customers = [User(id="1", name="Item 1"), User(id="2", name="Item 2")]

    return customers
