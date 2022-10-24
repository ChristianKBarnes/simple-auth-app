import datetime
from typing import Dict, List
from faker import Faker
from tortoise.expressions import Q

from app.schemas.student import StudentCreate, StudentUpdate
from app.models.student import Student
from app.api.crud import Student_Pydantic
from app.models.guardian import Guardian
from app.models.student_attendance import StudentAttendance

fake = Faker()


async def post(payload: StudentCreate) -> dict | None:
    student_code = await generate_student_code()

    student = await Student.create(
        student_code=student_code,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
    )

    if payload.guardians:
        guardians = await Guardian.filter(id__in=payload.guardians)

        for guardian in guardians:
            await student.guardians.add(guardian)

    return student


async def get(id: int) -> dict | None:
    student = await Student.get_or_none(id=id, deleted_at=None)

    if student:
        return student
    return None


async def get_student_by_student_code(student_code: str) -> dict | None:
    student = await Student.get_or_none(student_code=student_code, deleted_at=None)

    if student:
        return student
    return None


async def get_student_relation_by_student_code(
    student_code: str, relation: str
) -> Dict | None:
    student = await Student.get(
        student_code=student_code, deleted_at=None
    ).prefetch_related(relation)

    return student


async def get_student_attendace_by_student_code(student_code: str) -> Dict | None:
    student = await Student.get(
        student_code=student_code, deleted_at=None
    ).prefetch_related("attendance")

    attendance = await student.attendance

    return attendance


async def get_all() -> List:
    students = await Student.filter(deleted_at=None)

    return students


async def delete(id: int) -> int | None:
    student = await Student.filter(Q(id=id) & Q(deleted_at=None)).update(
        deleted_at=datetime.datetime.now()
    )

    if student:
        return student
    return None


async def put(id: int, payload: StudentUpdate) -> Dict | None:
    data = payload.dict(exclude_unset=True)

    if "guardians" in data:
        data.pop("guardians")

    student = await Student.filter(Q(id=id) & Q(deleted_at=None)).update(**data)

    if payload.guardians:
        st = await Student.get(id=id, deleted_at=None)
        guardians = await Guardian.filter(id__in=payload.guardians)

        if guardians:
            for guardian in guardians:
                await st.guardians.add(guardian)

    if student:
        updated_student = await Student.filter(id=id).first()

        return updated_student
    return None


async def generate_student_code() -> str:
    student_count = await Student.all().count() + 1
    pad = str(student_count).zfill(8)

    return "LS{0}-{1}".format(pad, fake.random_number(3))


async def has_checked_in(student: int, date) -> bool:
    attendance = await StudentAttendance.get_or_none(student=student, date=date)

    if attendance:
        return True

    return False


async def has_not_checked_out(student: int, date) -> bool:
    attendance = await StudentAttendance.get_or_none(
        student=student, date=date, checkout_at=None
    )

    if attendance:
        return True

    return False


async def check_in(student: int, date):
    attendance = await StudentAttendance.create(
        student_id=student, date=date, checkin_at=datetime.datetime.now()
    )

    return attendance


async def check_out(student: int, date):
    attendance = await StudentAttendance.filter(
        Q(student=student) & Q(date=date)
    ).update(checkout_at=datetime.datetime.now())

    return attendance


async def get_student_guardians_emails(student: str):
    student = await get_student_relation_by_student_code(student, "guardians")
    guardians = await student.guardians

    return [
        {"email": guardian.email, "name": guardian.first_name}
        for guardian in guardians
        if guardian.email is not None
    ]
