import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DATABASE_URL")

db_test_url =  os.environ.get("DATABASE_TEST_URL")

MODELS = [
    "app.models.user",
    "app.models.student",
    "app.models.guardian",
    "app.models.student_attendance",
    "app.models.teacher",
    "app.models.teacher_attendance",
    "aerich.models",
]