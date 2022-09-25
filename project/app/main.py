import logging

from fastapi import FastAPI
from starlette.exceptions import HTTPException

from app.db import init_db
from app.router.api import api_router
from app.api.errors.http_error import http_error_handler

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)
    application.add_exception_handler(HTTPException, http_error_handler)

    return application


app = create_application()


@app.on_event("startup") # pragma: no cover
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown") # pragma: no cover
async def shutdown_event():
    log.info("Shutting down...")
