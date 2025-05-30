import http

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app import settings, logger
from app.core.exception.exceptions import AppException, ProviderNotFoundException, AuthException
from app.schemas.base import ResponseSchema


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(exc, exc_info=settings.log.exc_info)
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseSchema(
                error=str(exc),
                message="",
                status_code=http.HTTPStatus.BAD_REQUEST,
                data=None
            ).model_dump()
        )

    @app.exception_handler(AuthException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error(exc, exc_info=settings.log.exc_info)
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseSchema(
                error=str(exc),
                message=exc.message,
                status_code=exc.status_code,
                data=None
            ).model_dump()
        )

    @app.exception_handler(ProviderNotFoundException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error(exc, exc_info=settings.log.exc_info)
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseSchema(
                error=exc.message,
                message="",
                status_code=exc.status_code,
                data=None
            ).model_dump()
        )
