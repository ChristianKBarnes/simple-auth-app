import datetime
from typing import List

from tortoise.expressions import Q

from app.schemas.user import UserBase, UserCreate
from app.models.user import User
from app.utils import get_password_hash


async def post(payload: UserCreate) -> dict | None:
    password = get_password_hash(payload.password)
    user = User(email=payload.email, name=payload.name, password=password)
    await user.save()

    return user


async def get(id: int) -> dict | None:
    user = await User.filter(Q(id=id) & Q(deleted_at=None)).first()
    if user:
        return user
    return None


async def get_user_by_email(email: str) -> dict | None:
    user = await User.filter(Q(email=email) & Q(deleted_at=None)).first()
    if user:
        return user
    return None


async def get_all() -> List:
    users = await User.filter(deleted_at=None).values()
    return users


async def delete(id: int) -> int | None:
    user = await User.filter(Q(id=id) & Q(deleted_at=None)).update(
        deleted_at=datetime.datetime.now()
    )
    if user:
        return user
    return None


async def put(id: int, payload: UserBase) -> dict | None:
    user = await User.filter(Q(id=id) & Q(deleted_at=None)).update(
        email=payload.email, name=payload.name
    )
    if user:
        updated_user = await User.filter(id=id).first()
        return updated_user
    return None
