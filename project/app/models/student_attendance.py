from tortoise import fields
from tortoise.models import Model

from app.models.student import Student
from app.traits.models.timestamp import Timestamp


class StudentAttendance(Model, Timestamp):
    id = fields.IntField(pk=True)
    student: fields.ForeignKeyRelation[Student] = fields.ForeignKeyField(
        "models.Student",
        related_name="attendance",
    )
    date = fields.DateField()
    checkin_at = fields.DatetimeField(auto_now_add=False, null=True)
    checkout_at = fields.DatetimeField(auto_now_add=False, null=True)

    class Meta:
        table = "student_attendace"
