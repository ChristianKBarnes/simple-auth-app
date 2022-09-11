from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    email: EmailStr

    # @validator("password")
    # def passwords_strength(cls, input_password):

    #     return input_passwor


class UserResponse(UserBase):
    id: int
