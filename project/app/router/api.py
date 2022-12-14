from fastapi import APIRouter, Depends

from app.api import ping, users, auth, students, guardians, attendance, teachers, teacher_attendance
from app.providers.AuthenticationProvider import AuthenticationProvider

api_router = APIRouter()
PROTECTED = Depends(AuthenticationProvider(scopes=["*"]))

api_router.include_router(ping.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(attendance.router, prefix="/student-attendance", tags=["student attendance"])
api_router.include_router(guardians.router, prefix="/guardians", tags=["guardians"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(teacher_attendance.router, prefix="/teachers-attendance", tags=["teacher attendance"])
