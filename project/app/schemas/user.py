from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    email: EmailStr


class UserResponse(UserBase):
    id: int


class UserUpdate(UserBase):
    name: str | None
    email: EmailStr | None
