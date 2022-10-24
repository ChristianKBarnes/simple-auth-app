import os, pytest

from fastapi_mail import ConnectionConfig
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from faker import Faker

from app.config.app import Settings, get_settings
from app.main import create_application
from app.config import database
from app.api.auth import get_current_active_user
from app.models.student import Student
from app.models.guardian import Guardian

fake = Faker()


def get_settings_override():
    email_configuration = ConnectionConfig(
        SUPPRESS_SEND=1,
        MAIL_TLS=True,
        MAIL_SSL=False,
        TEMPLATE_FOLDER=os.getenv("MAIL_TEMPLATE_FOLDELR"),
    )

    return Settings(
        testing=1,
        database_url=database.db_test_url,
        environment="testing",
        email_configuration=email_configuration,
    )


def get_current_active_user_override():
    return {
        "email": fake.email(),
        "name": fake.name(),
    }


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
        pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
        pytest.param(
            ("trio", {"restrict_keyboard_interrupt_to_checkpoints": True}), id="trio"
        ),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture
async def create_student(request) -> Student:
    """create a student in the db"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    other_names = fake.first_name() if fake.boolean() else None
    student_code = "LS-{}".format(fake.random_number(10))

    student = Student(
        first_name=first_name,
        last_name=last_name,
        other_names=other_names,
        student_code=student_code,
    )
    await student.save()

    return student


@pytest.fixture
async def create_guardian(request) -> Guardian:
    """create a guardian in the db"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.unique.phone_number()
    email = fake.unique.email()

    guardian = Guardian(first_name=first_name, last_name=last_name, phone=phone, email=email)
    await guardian.save()

    return guardian


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_current_active_user] = get_current_active_user_override
    Tortoise._drop_databases
    register_tortoise(
        app,
        db_url=database.db_test_url,
        modules={"models": database.MODELS[:-1]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
