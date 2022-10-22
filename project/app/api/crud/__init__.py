from app.config import database
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.student import Student
from app.models.student_attendance import StudentAttendance

Tortoise.init_models(database.MODELS, "models")

Student_Pydantic = pydantic_model_creator(Student)
Attendance_Pydantic = pydantic_model_creator(StudentAttendance)
