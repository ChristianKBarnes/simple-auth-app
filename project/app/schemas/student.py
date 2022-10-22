from typing import Any, List
from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    other_names: str | None
    email: EmailStr | None


class StudentCreate(StudentBase):
    guardians: List[int] | None


class StudentUpdate(StudentBase):
    first_name: str | None
    last_name: str | None
    guardians: List[int] | None


class BaseResponse(StudentBase):
    id: int
    student_code: str | None

 
class AllStudentsResponse(BaseModel):
    students: List[BaseResponse]

class GetStudentResponse(BaseModel):
    student: BaseResponse
