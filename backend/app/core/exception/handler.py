import http

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app import settings, logger
from app.core.exception.exceptions import AppException, AuthException, ProviderModelCredentialNotProvidedException
from app.schemas.base import ResponseSchema


def register_exception_handlers(app: FastAPI):
    @app.middleware("http")
    async def catch_all_exceptions_middleware(request: Request, call_next) -> JSONResponse:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:

            # 这里可以打印日志
            if isinstance(exc, SQLAlchemyError):
                exc = Exception("database query: pls check log")
            logger.error(exc, exc_info=settings.log.exc_info)
            return JSONResponse(
                status_code=400,
                content=ResponseSchema(
                    error=str(exc),
                    message="异常错误",
                    status_code=http.HTTPStatus.BAD_REQUEST,
                    data=None
                ).model_dump()
            )

    # @app.exception_handler(Exception)
    # async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    #     if isinstance(exc, SQLAlchemyError):
    #         e = Exception("database query: pls check log")
    #     logger.error(exc, exc_info=settings.log.exc_info)
    #     return JSONResponse(
    #         status_code=http.HTTPStatus.BAD_REQUEST,
    #         content=ResponseSchema(
    #             error=str(exc),
    #             message="",
    #             status_code=http.HTTPStatus.BAD_REQUEST,
    #             data=None
    #         ).model_dump()
    #     )

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

    @app.exception_handler(ProviderModelCredentialNotProvidedException)
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
