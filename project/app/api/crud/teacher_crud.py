import datetime
from typing import Dict, List
from faker import Faker
from tortoise.expressions import Q

from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.models.teacher import Teacher
from app.models.guardian import Guardian
from app.models.teacher_attendance import TeacherAttendance

fake = Faker()


async def post(payload: TeacherCreate) -> dict | None:
    teacher_code = await generate_teacher_code()

    teacher = await Teacher.create(
        teacher_code=teacher_code,
        first_name=payload.first_name,
        last_name=payload.last_name,
        other_names=payload.other_names,
        phone=payload.phone,
        email=payload.email,
    )

    return teacher


async def get(id: int) -> dict | None:
    teacher = await Teacher.get_or_none(id=id, deleted_at=None)

    if teacher:
        return teacher
    return None


async def get_teacher_by_teacher_code(teacher_code: str) -> dict | None:
    teacher = await Teacher.get_or_none(teacher_code=teacher_code, deleted_at=None)

    if teacher:
        return teacher
    return None


async def get_teacher_attendace_by_teacher_code(teacher_code: str) -> Dict | None:
    teacher = await Teacher.get(
        teacher_code=teacher_code, deleted_at=None
    ).prefetch_related("attendance")

    attendance = await teacher.attendance

    return attendance


async def get_all() -> List:
    teachers = await Teacher.filter(deleted_at=None)

    return teachers


async def delete(id: int) -> int | None:
    teacher = await Teacher.filter(Q(id=id) & Q(deleted_at=None)).update(
        deleted_at=datetime.datetime.now()
    )

    if teacher:
        return teacher
    return None


async def restore(id: int) -> int | None:
    teacher = await Teacher.filter(Q(id=id)).update(deleted_at=None)

    if teacher:
        return teacher
    return None

async def put(id: int, payload: TeacherUpdate) -> dict | None:
    teacher = await Teacher.filter(Q(id=id) & Q(deleted_at=None)).update(
        **payload.dict(exclude_unset=True)
    )

    if teacher:
        updated_teacher = await Teacher.filter(id=id).first()
        return updated_teacher
    return None

async def generate_teacher_code() -> str:
    teacher_count = await Teacher.all().count() + 1
    pad = str(teacher_count).zfill(8)

    return "LS-{0}-{1}-T".format(pad, fake.random_number(2))


async def has_checked_in(teacher: int, date) -> bool:
    attendance = await TeacherAttendance.get_or_none(teacher=teacher, date=date)

    if attendance:
        return True

    return False


async def has_not_checked_out(teacher: int, date) -> bool:
    attendance = await TeacherAttendance.get_or_none(
        teacher=teacher, date=date, checkout_at=None
    )

    if attendance:
        return True

    return False


async def check_in(teacher: int, date):
    attendance = await TeacherAttendance.create(
        teacher_id=teacher, date=date, checkin_at=datetime.datetime.now()
    )

    return attendance


async def check_out(teacher: int, date):
    attendance = await TeacherAttendance.filter(
        Q(teacher=teacher) & Q(date=date)
    ).update(checkout_at=datetime.datetime.now(), updated_at=datetime.datetime.now())

    return attendance
