from typing import Dict

from tortoise.expressions import Q
from app.api.crud import Attendance_Pydantic
from app.models.student_attendance import StudentAttendance


async def get_checked_in_students(date: str) -> Dict | None:
    attendance = await Attendance_Pydantic.from_queryset(
        StudentAttendance.filter(
            Q(date=date) & Q(deleted_at=None) & Q(checkin_at__not_isnull=True)
        )
    )

    return attendance


async def get_checked_out_students(date: str) -> Dict | None:
    attendance = await Attendance_Pydantic.from_queryset(
        StudentAttendance.filter(
            Q(date=date) & Q(deleted_at=None) & Q(checkout_at__not_isnull=True)
        )
    )

    return attendance
