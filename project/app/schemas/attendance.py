from typing import Any, List, TypedDict
from datetime import date, datetime
from pydantic import BaseModel

from app.schemas.student import BaseResponse as StudentBaseResponse
from app.schemas.teacher import BaseResponse as TeacherBaseResponse


class AttendanceShemaBase(BaseModel):
    checkin_at: date | None
    checkout_at: date | None
    date: date
    created_at: datetime
    updated_at: datetime
    student: StudentBaseResponse


class AttendaceResponse(BaseModel):
    attendance: List[AttendanceShemaBase]


class TeacherAttendanceShemaBase(BaseModel):
    checkin_at: date | None
    checkout_at: date | None
    date: date
    created_at: datetime
    updated_at: datetime
    teacher: TeacherBaseResponse


class TeacherAttendaceResponse(BaseModel):
    attendance: List[TeacherAttendanceShemaBase]
