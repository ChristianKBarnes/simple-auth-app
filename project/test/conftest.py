import os

import pytest
from starlette.testclient import TestClient
from dotenv import load_dotenv

from app.config.app import Settings, get_settings
from app.main import create_application
from app.config import database

load_dotenv()


def get_settings_override():
    return Settings(testing=1, database_url=database.db_test_url, environment="testing")


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
