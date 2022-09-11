from fastapi import APIRouter

from app.api import ping, users, auth

api_router = APIRouter()

api_router.include_router(ping.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
