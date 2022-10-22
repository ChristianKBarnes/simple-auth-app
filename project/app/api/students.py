import datetime, io
from typing import Dict, List

import qrcode
from fastapi import APIRouter, HTTPException, status
from starlette.responses import StreamingResponse

from app.api.crud import student_crud
from app.schemas.student import StudentCreate, AllStudentsResponse, GetStudentResponse, StudentUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=AllStudentsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Students",
)
async def index(student_code: str = None) -> AllStudentsResponse:
    if student_code:
        student = await student_crud.get_student_by_student_code(student_code)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
            )

        return {"students": [student]}
    students = await student_crud.get_all()

    return {"students": students}


@router.get(
    "/{id}",
    response_model=GetStudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Student Details",
)
async def show(id: int) -> GetStudentResponse:
    student = await student_crud.get(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"student": student}


@router.post(
    "/",
    response_model=GetStudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Student",
)
async def store(payload: StudentCreate) -> GetStudentResponse:
    student = await student_crud.post(payload)

    return {"student": student}

@router.put("/{id}", status_code=200, summary="Update Student Details")
async def update(id: int, payload: StudentUpdate) -> Dict:
    student = await student_crud.put(id, payload)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student updated successfully"}


@router.delete("/{id}", status_code=204, summary="Delete Student")
async def delete(id: int):
    student = await student_crud.delete(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student deleted successfully"}


@router.post(
    "/{student_code}/check-in",
    status_code=status.HTTP_200_OK,
    summary="Check In Student",
    description="You can check in a student once daily. You cannot check in a student after you have checked the student in.",
)
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


@router.post(
    "/{student_code}/check-out",
    status_code=status.HTTP_200_OK,
    summary="Check Out Student",
    description="You can check in a student once daily. You cannot check in a student after you have checked the student in.",
)
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


@router.get(
    "/{student_code}/qr-code",
    status_code=status.HTTP_200_OK,
    summary="Generate Student QR Code",
)
async def qr_code(student_code: str):
    student = await student_crud.get_student_by_student_code(student_code)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Student Not Found"
        )

    img = qrcode.make(student_code)
    response_buffer = io.BytesIO()
    img.save(response_buffer)
    response_buffer.seek(0)
    return StreamingResponse(response_buffer, media_type="image/jpeg")


@router.get(
    "/{student_code}/attendance",
    status_code=status.HTTP_200_OK,
    summary="Get Student Attendance",
)
async def attendance(student_code: str):
    student_attendance = await student_crud.get_student_attendace_by_student_code(
        student_code
    )

    return {"attendance": student_attendance}
