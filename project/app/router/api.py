from fastapi import APIRouter, Depends

from app.api import ping, users, auth, students, guardians
from app.providers.AuthenticationProvider import AuthenticationProvider

api_router = APIRouter()
PROTECTED = Depends(AuthenticationProvider(scopes=["*"]))

api_router.include_router(ping.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(guardians.router, prefix="/guardians", tags=["guardians"])
