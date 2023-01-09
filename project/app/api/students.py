import datetime
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status, UploadFile
from starlette.responses import StreamingResponse

from app.api.crud import student_crud
from app.schemas.student import (
    StudentCreate,
    AllStudentsResponse,
    GetStudentResponse,
    StudentUpdate,
)
from app.utils import send_email, send_multiple_emails, generate_qrcode
from app.config.app import Settings, get_settings
from app.logging import log

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


@router.put("/{id}", status_code=status.HTTP_200_OK, summary="Update Student Details")
async def update(id: int, payload: StudentUpdate) -> Dict:
    student = await student_crud.put(id, payload)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Student")
async def delete(id: int):
    student = await student_crud.delete(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student deleted successfully"}


@router.put("/restore/{id}", status_code=status.HTTP_200_OK, summary="Restore Student")
async def restore(id: int):
    student = await student_crud.restore(id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    return {"detail": "Student restored successfully"}


@router.post(
    "/{student_code}/check-in",
    status_code=status.HTTP_200_OK,
    summary="Check In Student",
    description="You can check in a student once daily. You cannot check in a student after you have checked the student in.",
)
async def check_in(
    student_code: str,
    background_tasks: BackgroundTasks,
    request: Request,
    settings: Settings = Depends(get_settings),
):
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
        guardians = await student_crud.get_student_guardians_emails(student_code)

        if guardians:
            send_multiple_emails(
                background_tasks,
                subject="Check In Notification",
                recipients=guardians,
                body={
                    "url_for": request.url_for,
                    "ward": student.fullname(),
                    "checkin_at": date.strftime("%A, %d %B, %Y %H:%M %p"),
                    "year": date.year,
                },
                template_name="check_in.html",
                settings=settings,
            )

        return {"detail": "Student check in successful"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
    )


@router.post(
    "/{student_code}/check-out",
    status_code=status.HTTP_200_OK,
    summary="Check Out Student",
    description="You can check in a student once daily. You cannot check in a student after you have checked the student in.",
)
async def check_out(
    student_code: str,
    background_tasks: BackgroundTasks,
    request: Request,
    settings: Settings = Depends(get_settings),
):
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
            guardians = await student_crud.get_student_guardians_emails(student_code)

            if guardians:
                send_multiple_emails(
                    background_tasks,
                    subject="Check Out Notification",
                    recipients=guardians,
                    body={
                        "url_for": request.url_for,
                        "ward": student.fullname(),
                        "checkin_at": date.strftime("%A, %d %B, %Y %H:%M %p"),
                        "year": date.year,
                    },
                    template_name="check_out.html",
                    settings=settings,
                )

            return {"detail": "Student check out successful"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student has already checked out",
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
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
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not Found"
        )

    qrcode_buffer = generate_qrcode(student_code)
    return StreamingResponse(qrcode_buffer, media_type="image/jpeg")


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


@router.get(
    "/{student_code}/guardians",
    status_code=status.HTTP_200_OK,
    summary="Get Student Guardians",
)
async def guardians(student_code: str):
    student = await student_crud.get_student_relation_by_student_code(
        student_code, "guardians"
    )
    guardians = await student.guardians

    return {"guardians": guardians}


@router.post(
    "/{student_code}/welcome",
    status_code=status.HTTP_200_OK,
    summary="Welcome student",
)
async def welcome(
    background_tasks: BackgroundTasks,
    student_code: str,
    request: Request,
    settings: Settings = Depends(get_settings),
):
    student = await student_crud.get_student_by_student_code(student_code)
    guardians = await student_crud.get_student_guardians_emails(student_code)

    if guardians:
        attachment = UploadFile(filename="QR Code", file=generate_qrcode(student_code), content_type="image/jpeg")

        send_email(
            background_tasks,
            subject="Welcome to Little Steps Montessori",
            email_to=list(map(lambda guardian: guardian["email"], guardians)),
            body={
                "url_for": request.url_for,
                "ward": student.fullname(),
            },
            template_name="welcome.html",
            settings=settings,
            attachments=[attachment],
        )

    return {"detail": "Student welcomed successfully."}
