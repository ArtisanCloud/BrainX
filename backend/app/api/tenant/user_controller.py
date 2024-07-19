from fastapi import APIRouter, Depends

from app.api.middleware.auth import get_session_user
from app.models.originaztion.user import User

from app.schemas.tenant.user import ResponseGetUser

router = APIRouter()


@router.get("/get")
async def api_get_user(
        current_user: User = Depends(get_session_user)
) -> ResponseGetUser:
    """
    Get all documents or documents by their ids
    """

    return current_user
