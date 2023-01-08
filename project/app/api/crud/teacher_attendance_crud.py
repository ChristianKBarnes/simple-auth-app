from typing import Dict

from tortoise.expressions import Q
from app.api.crud import Attendance_Pydantic
from app.models.teacher_attendance import TeacherAttendance


async def get_checked_in_teachers(date: str) -> Dict | None:
    attendance = await Attendance_Pydantic.from_queryset(
        TeacherAttendance.filter(
            Q(date=date) & Q(deleted_at=None) & Q(checkin_at__not_isnull=True)
        )
    )

    return attendance


async def get_checked_out_teachers(date: str) -> Dict | None:
    attendance = await Attendance_Pydantic.from_queryset(
        TeacherAttendance.filter(
            Q(date=date) & Q(deleted_at=None) & Q(checkout_at__not_isnull=True)
        )
    )

    return attendance
