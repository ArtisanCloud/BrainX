from fastapi import APIRouter, Depends
import logging

from app.api.middleware.auth import get_current_user
from app.models.originaztion.user import User

from app.schemas.user import ResponseGetUser

router = APIRouter()


@router.get("/get")
async def api_get_user(
        current_user: User = Depends(get_current_user)
) -> ResponseGetUser:
    """
    Get all documents or documents by their ids
    """

    user = User()

    return user
