from fastapi import APIRouter
from typing import List
from app.models.tenant.customer import Customer

router = APIRouter()


@router.get("/")
async def get_customers() -> List[Customer]:
    """
    Get all documents or documents by their ids
    """
    customers = [Customer(Id="1", Name="Item 1"), Customer(Id="2", Name="Item 2")]
    return customers
