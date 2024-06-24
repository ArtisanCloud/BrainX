import asyncio

from fastapi import APIRouter
from starlette.requests import Request

from app.logger import logger
from app.schemas.base import ResponseSchema

router = APIRouter()


@router.get("/test/timeout")
async def api_test_timeout(request: Request) -> ResponseSchema:
    timeout_seconds = int(request.query_params.get("timeout", 5))
    print(f"Timeout seconds: {timeout_seconds}")

    async def loop_task():
        for i in range(timeout_seconds):
            # Your code here
            logger.info(f"Loop iteration {i + 1}")
            await asyncio.sleep(1)  # Wait for 1 second

    try:
        await asyncio.wait_for(loop_task(), timeout=timeout_seconds)
    except asyncio.TimeoutError:
        logger.info("Timeout reached")
    except Exception as e:
        logger.error(f"Error in loop: {str(e)}")

    return ResponseSchema(
        error=f'Timeout: {timeout_seconds} '
    )
