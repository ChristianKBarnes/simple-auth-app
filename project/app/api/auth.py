import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt

from app.api.crud import user_crud
from app.schemas.auth import (
    AuthResponseSchema,
    RegisterPayloadSchema,
    LoginPayloadSchema,
)
from app.config.app import (
    app_secret,
    app_hash_algorithm,
    # app_access_token_expire_minutes,
)
from app.models.user import User
from app.utils import create_access_token, verify_password, oauth2_scheme

router = APIRouter()
log = logging.getLogger("uvicorn")


@router.post("/register", response_model=AuthResponseSchema, status_code=201)
async def register(payload: RegisterPayloadSchema) -> AuthResponseSchema:
    user = await user_crud.post(payload)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token({"sub": user.email}, access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login", response_model=AuthResponseSchema, status_code=200)
async def login(form_data: LoginPayloadSchema) -> AuthResponseSchema:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


async def authenticate_user(username: str, password: str):
    user = await user_crud.get_user_by_email(username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str) -> User:  # pragma: no cover
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, app_secret, algorithms=[app_hash_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except AttributeError:
        raise credentials_exception
    user = await user_crud.get_user_by_email(email=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(authorization_token: str) -> User:  # pragma: no cover
    authorized_user = await get_current_user(authorization_token)

    if not authorized_user or authorized_user.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )
    return authorized_user
