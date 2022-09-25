from app.config import database
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.student import Student

Tortoise.init_models(database.MODELS, "models")

Student_Pydantic = pydantic_model_creator(Student)
