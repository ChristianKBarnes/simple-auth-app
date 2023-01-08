import datetime

from fastapi import APIRouter, status

from app.api.crud import teacher_attendance_crud
from app.schemas.attendance import TeacherAttendaceResponse


router = APIRouter()


@router.get(
    "/checked-in",
    response_model=TeacherAttendaceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Checked In Teachers",
    description="Get checked in teacher for a given date. Date is defaulted to today.",
)
async def checked_in_teachers(date: str = None) -> TeacherAttendaceResponse:
    check_date = (
        date if date is not None else datetime.datetime.now().strftime("%Y-%m-%d")
    )

    attendance = await teacher_attendance_crud.get_checked_in_teachers(check_date)

    return {"attendance": attendance}


@router.get(
    "/checked-out",
    response_model=TeacherAttendaceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Checked Out Teachers",
    description="Get checked out teacher for a given date. Date is defaulted to today.",
)
async def checked_out_teachers(date: str = None) -> TeacherAttendaceResponse:
    check_date = (
        date if date is not None else datetime.datetime.now().strftime("%Y-%m-%d")
    )

    attendance = await teacher_attendance_crud.get_checked_out_teachers(check_date)

    return {"attendance": attendance}
