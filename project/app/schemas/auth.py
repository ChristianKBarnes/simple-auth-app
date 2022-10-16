from typing import Dict, TypedDict
from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    name: str
    email: EmailStr


class RegisterPayloadSchema(AuthBase):
    password: str


class LoginPayloadSchema(BaseModel):
    username: EmailStr
    password: str


class UserSchema(TypedDict):
    id: int
    name: str
    email: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserSchema
