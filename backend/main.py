import importlib
import pkgutil

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

import app.api.routers as routers_pkg
from app.infrastructure.config import settings
from app.infrastructure.database import engine
from app.domain.exceptions.base import DomainException
from app.api.exception_handlers import (
    domain_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Project Manager API",
        description="Internal system to manage projects, team members and assignments",
        version="1.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for _, name, _ in pkgutil.iter_modules(routers_pkg.__path__):
        module = importlib.import_module(f"app.api.routers.{name}")
        if hasattr(module, "router"):
            app.include_router(module.router, prefix="/api")

    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    @app.get("/health", tags=["Health"])
    async def health():
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return {"status": "ok", "database": "ok"}
        except Exception:
            return JSONResponse(
                status_code=503,
                content={"status": "error", "database": "unreachable"},
            )

    return app


app = create_app()
