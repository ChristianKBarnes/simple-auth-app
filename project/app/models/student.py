from tortoise.models import Model
from tortoise import fields, Tortoise

from app.traits.models.timestamp import Timestamp
from app.models.guardian import Guardian
from app.config import database


class Student(Model, Timestamp):
    id = fields.IntField(pk=True)
    student_code = fields.CharField(119, null=True, unique=True)
    first_name = fields.CharField(119, null=False)
    last_name = fields.CharField(119, null=False)
    other_names = fields.CharField(119, null=True)
    email = fields.CharField(119, unique=True, null=True)
    guardians: fields.ManyToManyRelation[Guardian] = fields.ManyToManyField(
        "models.Guardian", related_name="guardians", through="student_guardian"
    )

    def __str__(self):
        return self.fullname()

    def fullname(self):  # pragma: no cover
        if self.other_names:
            return "{0} {1} {2} ".format(
                self.first_name, self.other_names, self.last_name
            )
        return "{0} {1}".format(self.first_name, self.last_name)
    

    class PydanticMeta:
        exclude = ["created_at", "deleted_at"]

