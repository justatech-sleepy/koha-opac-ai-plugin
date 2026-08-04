"""
main.py — FastAPI application factory for the Koha OPAC AI Assistant backend.

Start the server:
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pymysql

from app.core.config import settings
from app.routers import chat, search, health, vision

# -----------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("koha_opac_ai")

# -----------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered chatbot backend for the Koha OPAC AI Assistant plugin.",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# -----------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# -----------------------------------------------------------------------
# Exception handlers
# -----------------------------------------------------------------------

@app.exception_handler(pymysql.Error)
async def db_exception_handler(request: Request, exc: pymysql.Error):
    logger.error("Database error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=503,
        content={
            "error": "database_unavailable",
            "message": "The library catalogue is temporarily unavailable. Please try again later.",
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
        },
    )

# -----------------------------------------------------------------------
# Routers
# -----------------------------------------------------------------------
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(search.router)
app.include_router(vision.router)

# -----------------------------------------------------------------------
# Startup / Shutdown events
# -----------------------------------------------------------------------

@app.on_event("startup")
async def on_startup():
    logger.info(
        "%s v%s starting up (search_engine=%s, debug=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.SEARCH_ENGINE,
        settings.DEBUG,
    )


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("%s shutting down", settings.APP_NAME)
