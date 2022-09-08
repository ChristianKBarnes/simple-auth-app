from fastapi import APIRouter, Depends
from starlette import responses

from app.config.app import Settings, get_settings

router = APIRouter()


@router.get("/")
async def root():
    return responses.RedirectResponse("/redoc")


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
