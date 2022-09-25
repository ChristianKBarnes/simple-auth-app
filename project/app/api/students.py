import datetime
from typing import Dict, List
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.crud import student_crud
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter()
log = logging.getLogger("uvicorn")


@router.get("/", response_model=List, status_code=200)
async def index(student_code: str = None) -> List:
    if student_code:
        student = await student_crud.get_student_by_student_code(student_code)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
            )

        return [student]
    students = await student_crud.get_all()

    return students


@router.get("/{id}", status_code=200)
async def show(id: int):
    student = await student_crud.get(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return student


@router.post("/", response_model=StudentResponse, status_code=201)
async def store(payload: StudentCreate) -> StudentResponse:
    student = await student_crud.post(payload)

    return {
        "id": student.id,
        "student_code": student.student_code,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "other_names": student.other_names,
        "email": student.email,
    }


@router.put("/{id}", status_code=200)
async def update(id: int, payload: StudentUpdate) -> Dict:
    student = await student_crud.put(id, payload)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student updated successfully"}


@router.delete("/{id}", status_code=204)
async def delete(id: int):
    student = await student_crud.delete(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student deleted successfully"}


@router.post("/{student_code}/check-in", status_code=status.HTTP_200_OK)
async def check_in(student_code: str):
    student = await student_crud.get_student_by_student_code(student_code)
    date = datetime.datetime.now()

    if student:
        has_checked_in = await student_crud.has_checked_in(
            student.id, date.strftime("%Y-%m-%d")
        )

        if has_checked_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student has already checked in",
            )

        await student_crud.check_in(student.id, date.strftime("%Y-%m-%d"))
        # send notification to student guardians.

        return {"detail": "Student check in successful"}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Student Not Found"
    )


@router.post("/{student_code}/check-out", status_code=status.HTTP_200_OK)
async def check_out(student_code: str):
    student = await student_crud.get_student_by_student_code(student_code)
    date = datetime.datetime.now()

    if student:
        has_checked_in = await student_crud.has_checked_in(
            student.id, date.strftime("%Y-%m-%d")
        )

        if not has_checked_in:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student has not checked in",
            )

        has_not_checked_out = await student_crud.has_not_checked_out(
            student.id, date.strftime("%Y-%m-%d")
        )
        if has_not_checked_out:
            await student_crud.check_out(student.id, date.strftime("%Y-%m-%d"))

            # send notification to student guardians.
            return {"detail": "Student check out successful"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student has already checked out",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Student Not Found"
    )


@router.get("/{student_code}/qr-code", status_code=status.HTTP_200_OK)
async def qr_code(student_code: str):
    student = await student_crud.get_student_by_student_code(student_code)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Student Not Found"
        )

    # generate student qr code
    pass
