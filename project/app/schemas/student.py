from typing import Any, List
from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    other_names: str | None
    email: EmailStr | None
    guardians: List[int] | None


class StudentCreate(StudentBase):
    # student_code: str | None
    pass

class StudentResponse(StudentBase):
    id: int
    student_code: str | None


class StudentUpdate(StudentBase):
    first_name: str | None
    last_name: str | None

