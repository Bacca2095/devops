from datetime import datetime, timezone

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions.base import (
    DomainException,
    NotFoundException,
    ConflictException,
    BusinessRuleException,
)

_STATUS_MAP = {
    NotFoundException: 404,
    ConflictException: 409,
    BusinessRuleException: 422,
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def domain_exception_handler(
    request: Request, exc: DomainException
) -> JSONResponse:
    status_code = next(
        (code for exc_type, code in _STATUS_MAP.items() if isinstance(exc, exc_type)),
        500,
    )
    return JSONResponse(
        status_code=status_code,
        content={
            "code": exc.code,
            "detail": exc.message,
            "timestamp": exc.timestamp.isoformat(),
            "path": request.url.path,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    detail = {str(err["loc"][-1]): err["msg"] for err in exc.errors()}
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "detail": detail,
            "timestamp": _now(),
            "path": request.url.path,
        },
    )


async def unhandled_exception_handler(
    request: Request, _exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_ERROR",
            "detail": "An unexpected error occurred",
            "timestamp": _now(),
            "path": request.url.path,
        },
    )
