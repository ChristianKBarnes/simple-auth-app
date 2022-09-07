import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import UserCreate, UserResponse
from app.api.crud import user_crud
from app.api.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

log = logging.getLogger("uvicorn")


@router.post("/", response_model=UserResponse, status_code=201)
async def store(
    payload: UserCreate, current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_crud.post(payload)

    return {"id": user.id, "name": user.name, "email": user.email}


def test_post_request_without_body_returns_422(test_app_with_db):
    """body should have email and name"""
    response = test_app_with_db.post("/users/")
    assert response.status_code == 422
