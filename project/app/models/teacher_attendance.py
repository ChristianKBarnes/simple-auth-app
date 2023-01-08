from tortoise import fields
from tortoise.models import Model

from app.models.teacher import Teacher
from app.traits.models.timestamp import Timestamp


class TeacherAttendance(Model, Timestamp):
    id = fields.IntField(pk=True)
    teacher: fields.ForeignKeyRelation[Teacher] = fields.ForeignKeyField(
        "models.Teacher",
        related_name="attendance",
    )
    date = fields.DateField()
    checkin_at = fields.DatetimeField(auto_now_add=False, null=True)
    checkout_at = fields.DatetimeField(auto_now_add=False, null=True)

    class Meta:
        table = "teacher_attendace"

    class PydanticMeta:
        exclude = ["deleted_at"]
