from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from core.config import Settings
from core.logger import logger
from src.routers.base_router import base_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    yield

app = FastAPI(
    lifespan=lifespan,
    title=Settings.API_TITLE,
    version=Settings.PROJECT_VERSION,
    debug=False
)

app.include_router(base_router)


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    logger.error("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred. Please try again later.",
            "detail": str(exc)
        }
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
