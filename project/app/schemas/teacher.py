from typing import List
from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    other_names: str | None
    phone: str
    email: EmailStr | None


class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(TeacherBase):
    first_name: str | None
    last_name: str | None
    guardians: List[int] | None


class BaseResponse(TeacherBase):
    id: int
    teacher_code: str | None

class AllTeachersResponse(BaseModel):
    teachers: List[BaseResponse]

class GetTeacherResponse(BaseModel):
    teacher: BaseResponse
