import pytest

from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from faker import Faker

from app.config.app import Settings, get_settings
from app.main import create_application
from app.config import database
from app.api.auth import get_current_active_user

fake = Faker()


def get_settings_override():
    return Settings(testing=1, database_url=database.db_test_url, environment="testing")


def get_current_active_user_override():
    return {
        "email": fake.email(),
        "name": fake.name(),
    }


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
    register_tortoise(
        app,
        db_url=database.db_test_url,
        modules={"models": ["app.models.user"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
