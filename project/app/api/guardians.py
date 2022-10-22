from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.api.auth import get_current_active_user
from app.api.crud import guardian_crud
from app.models.user import User
from app.schemas.guardian import GuardianCreate, GuardianResponse, GuardianUpdate

router = APIRouter()


@router.get("/", response_model=List[GuardianResponse], status_code=status.HTTP_200_OK, summary="Get All Guardians")
async def index(email: str = None, phone: str = None) -> List[GuardianResponse]:
    if phone:
        guardian = await guardian_crud.get_guardian_by_phone(phone)

        if not guardian:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Guardian Not Found"
            )

        return [guardian]

    guardians = await guardian_crud.get_all()

    return guardians


@router.get("/{id}", response_model=GuardianResponse, status_code=status.HTTP_200_OK, summary="Get Guardians")
async def show(id: int) -> GuardianResponse:
    guardian = await guardian_crud.get(id)
    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guardian Not Found"
        )

    return guardian


@router.post("/", response_model=GuardianResponse, status_code=status.HTTP_201_CREATED, summary="Create New Guardian")
async def store(payload: GuardianCreate) -> GuardianResponse:
    guardian = await guardian_crud.post(payload)

    return {
        "id": guardian.id,
        "first_name": guardian.first_name,
        "last_name": guardian.last_name,
        "phone": guardian.phone,
        "other_names": guardian.other_names,
        "email": guardian.email,
        "identification_document_type": guardian.identification_document_type,
        "identification_document_number": guardian.identification_document_number,
        "identification_document_expiry": guardian.identification_document_expiry,
    }


@router.put("/{id}", status_code=status.HTTP_200_OK, summary="Update Guardian Details")
async def update(id: int, payload: GuardianUpdate) -> dict:
    guardian = await guardian_crud.put(id, payload)

    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guardian not found."
        )

    return {"message": "Guardian updated successfullyu"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Guardian")
async def delete(id: int):
    guardian = await guardian_crud.delete(id)

    if not guardian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guardian Not Found"
        )

    return {"message": "Guardian deleted successfully"}
