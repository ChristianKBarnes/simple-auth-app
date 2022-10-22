from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


class AuthBase(BaseModel):
    name: str
    email: EmailStr


class RegisterPayloadSchema(AuthBase):
    password: str


class LoginPayloadSchema(BaseModel):
    username: EmailStr
    password: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
