from fastapi import APIRouter
from typing import List
from app.models.tenant.customer import User

router = APIRouter()


@router.get("/")
async def get_customers() -> List[User]:
    """
    Get all documents or documents by their ids
    """
    customers = [User(Id="1", Name="Item 1"), User(Id="2", Name="Item 2")]
    return customers