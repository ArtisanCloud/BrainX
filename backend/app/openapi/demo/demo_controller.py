from fastapi import APIRouter

from app.schemas.base import ResponseSchema

router = APIRouter()


@router.post("/hello-world")
async def api_hello_world() -> ResponseSchema:
    data = ResponseSchema(
        message="hello world for openapi"
    )

    return data
