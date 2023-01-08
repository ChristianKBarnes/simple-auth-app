import datetime, io
from typing import Dict

import qrcode
from fastapi import APIRouter, HTTPException, status
from starlette.responses import StreamingResponse

from app.api.crud import teacher_crud
from app.schemas.teacher import (
    TeacherCreate,
    AllTeachersResponse,
    GetTeacherResponse,
    TeacherUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=AllTeachersResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Teachers",
)
async def index(teacher_code: str = None) -> AllTeachersResponse:
    if teacher_code:
        teacher = await teacher_crud.get_teacher_by_teacher_code(teacher_code)

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
            )

        return {"teachers": [teacher]}
    teachers = await teacher_crud.get_all()

    return {"teachers": teachers}


@router.get(
    "/{id}",
    response_model=GetTeacherResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Teacher Details",
)
async def show(id: int) -> GetTeacherResponse:
    teacher = await teacher_crud.get(id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
        )

    return {"teacher": teacher}


@router.post(
    "/",
    response_model=GetTeacherResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Teacher",
)
async def store(payload: TeacherCreate) -> GetTeacherResponse:
    teacher = await teacher_crud.post(payload)

    return {"teacher": teacher}


@router.put("/{id}", status_code=status.HTTP_200_OK, summary="Update Teacher Details")
async def update(id: int, payload: TeacherUpdate) -> Dict:
    teacher = await teacher_crud.put(id, payload)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
        )

    return {"detail": "Teacher updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Teacher")
async def delete(id: int):
    teacher = await teacher_crud.delete(id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
        )

    return {"detail": "Teacher deleted successfully"}


@router.put("/restore/{id}", status_code=status.HTTP_200_OK, summary="Restore Teacher")
async def restore(id: int):
    teacher = await teacher_crud.restore(id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
        )

    return {"detail": "Teacher restored successfully"}


@router.post(
    "/{teacher_code}/check-in",
    status_code=status.HTTP_200_OK,
    summary="Check In Teacher",
    description="You can check in a teacher once daily. You cannot check in a teacher after you have checked the teacher in.",
)
async def check_in(teacher_code: str):
    teacher = await teacher_crud.get_teacher_by_teacher_code(teacher_code)
    date = datetime.datetime.now()

    if teacher:
        has_checked_in = await teacher_crud.has_checked_in(
            teacher.id, date.strftime("%Y-%m-%d")
        )

        if has_checked_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Teacher has already checked in",
            )
        await teacher_crud.check_in(teacher.id, date.strftime("%Y-%m-%d"))

        return {"detail": "Teacher check in successful"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
    )


@router.post(
    "/{teacher_code}/check-out",
    status_code=status.HTTP_200_OK,
    summary="Check Out Teacher",
    description="You can check in a teacher once daily. You cannot check in a teacher after you have checked the teacher in.",
)
async def check_out(teacher_code: str):
    teacher = await teacher_crud.get_teacher_by_teacher_code(teacher_code)
    date = datetime.datetime.now()

    if teacher:
        has_checked_in = await teacher_crud.has_checked_in(
            teacher.id, date.strftime("%Y-%m-%d")
        )

        if not has_checked_in:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher has not checked in",
            )

        has_not_checked_out = await teacher_crud.has_not_checked_out(
            teacher.id, date.strftime("%Y-%m-%d")
        )
        if has_not_checked_out:
            await teacher_crud.check_out(teacher.id, date.strftime("%Y-%m-%d"))

            return {"detail": "Teacher check out successful"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher has already checked out",
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
    )


@router.get(
    "/{teacher_code}/qr-code",
    status_code=status.HTTP_200_OK,
    summary="Generate Teacher QR Code",
)
async def qr_code(teacher_code: str):
    teacher = await teacher_crud.get_teacher_by_teacher_code(teacher_code)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher Not Found"
        )

    img = qrcode.make(teacher_code)
    response_buffer = io.BytesIO()
    img.save(response_buffer)
    response_buffer.seek(0)
    return StreamingResponse(response_buffer, media_type="image/jpeg")


@router.get(
    "/{teacher_code}/attendance",
    status_code=status.HTTP_200_OK,
    summary="Get Teacher Attendance",
)
async def attendance(teacher_code: str):
    teacher_attendance = await teacher_crud.get_teacher_attendace_by_teacher_code(
        teacher_code
    )

    return {"attendance": teacher_attendance}

