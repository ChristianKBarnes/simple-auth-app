from typing import Any, List, TypedDict
from datetime import date, datetime
from pydantic import BaseModel

from app.schemas.student import BaseResponse


class AttendanceShemaBase(BaseModel):
    checkin_at: date | None
    checkout_at: date | None
    date: date
    created_at: datetime
    updated_at: datetime
    student: BaseResponse


class AttendaceResponse(BaseModel):
    attendance: List[AttendanceShemaBase]


class TeacherAttendanceShemaBase(BaseModel):
    checkin_at: date | None
    checkout_at: date | None
    date: date
    created_at: datetime
    updated_at: datetime
    student: BaseResponse


class TeacherAttendaceResponse(BaseModel):
    attendance: List[AttendanceShemaBase]
