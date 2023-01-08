from tortoise.models import Model
from tortoise import fields

from app.traits.models.timestamp import Timestamp


class Teacher(Model, Timestamp):
    id = fields.IntField(pk=True)
    teacher_code = fields.CharField(119, null=True, unique=True)
    first_name = fields.CharField(119, null=False)
    last_name = fields.CharField(119, null=False)
    other_names = fields.CharField(119, null=True)
    email = fields.CharField(119, unique=True, null=True)
    phone = fields.CharField(119, unique=True, null=False)
    identification_document_type = fields.CharField(119, null=True)
    identification_document_number = fields.CharField(119, null=True)
    identification_document_expiry = fields.DatetimeField(null=True)

    def __str__(self):  # pragma: no cover
        return self.fullname()

    def fullname(self):  # pragma: no cover
        if self.other_names:
            return "{0} {1} {2} ".format(
                self.first_name, self.other_names, self.last_name
            )
        return "{0} {1}".format(self.first_name, self.last_name)

    class PydanticMeta:
        exclude = ["created_at", "deleted_at"]
