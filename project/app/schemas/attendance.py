from typing import Any, List, TypedDict
from datetime import date, datetime
from pydantic import BaseModel

from app.schemas.student import BaseResponse


class AttendanceShemaBase(TypedDict):
    checkin_at: date | None
    checkout_at: date | None
    date: date
    updated_at: datetime
    student: BaseResponse

