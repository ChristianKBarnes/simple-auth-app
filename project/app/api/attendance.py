import datetime
from typing import List

from fastapi import APIRouter, status

from app.api.crud import attendance_crud
from app.schemas.attendance import AttendanceShemaBase


router = APIRouter()


@router.get(
    "/checked-in",
    response_model=List[AttendanceShemaBase],
    status_code=status.HTTP_200_OK,
    summary="Get Checked In Students",
    description="Get checked in student for a given date. Date is defaulted to today.",
)
async def checked_in_students(date: str = None) -> List[AttendanceShemaBase]:
    check_date = (
        date if date is not None else datetime.datetime.now().strftime("%Y-%m-%d")
    )

    attendance = await attendance_crud.get_checked_in_students(check_date)

    return attendance


@router.get(
    "/checked-out",
    response_model=List[AttendanceShemaBase],
    status_code=status.HTTP_200_OK,
    summary="Get Checked Out Students",
    description="Get checked out student for a given date. Date is defaulted to today.",
)
async def checked_out_students(date: str = None) -> List[AttendanceShemaBase]:
    check_date = (
        date if date is not None else datetime.datetime.now().strftime("%Y-%m-%d")
    )

    attendance = await attendance_crud.get_checked_out_students(check_date)

    return {"attendance": attendance}
