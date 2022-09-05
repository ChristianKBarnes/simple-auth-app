from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from app.traits.models.timestamp import Timestamp


class User(Model, Timestamp):
    id = fields.IntField(pk=True)
    name = fields.CharField(119, null=False)
    email = fields.CharField(119, unique=True, null=False)
    password = fields.CharField(119, null=False)

    def __int__(self):
        return self.id

SummarySchema = pydantic_model_creator(User)
