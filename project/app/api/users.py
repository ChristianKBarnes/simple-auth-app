import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.api.crud import user_crud
from app.api.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

log = logging.getLogger("uvicorn")


@router.get("/", response_model=List[UserResponse], status_code=200, summary="Get All Users")
async def index() -> List[UserResponse]:
    users = await user_crud.get_all()

    return users


@router.get("/{id}", response_model=UserResponse, status_code=200, summary="Get Student Details")
async def show(id: int) -> UserResponse:
    user = await user_crud.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Create New User",
)
async def store(payload: UserCreate) -> UserResponse:
    user = await user_crud.post(payload)

    return {"id": user.id, "name": user.name, "email": user.email}


@router.put("/{id}", status_code=200, summary="Update User Details")
async def update(id: int, payload: UserUpdate) -> dict:
    user = await user_crud.put(id, payload)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return {"message": "User updated successfully"}


@router.delete("/{id}", status_code=204, summary="Delete Exisiting User")
async def delete(id: int):
    user = await user_crud.delete(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    return {"message": "User deleted successfully"}
