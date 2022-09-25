from typing_extensions import assert_type
from faker import Faker

fake = Faker()


def test_get_request_returns_405(test_app_with_db):
    response = test_app_with_db.get("/auth/register")
    assert response.status_code == 405


def test_post_request_without_body_returns_422(test_app_with_db):
    response = test_app_with_db.post("/auth/register")
    assert response.status_code == 422


def test_register_with_invalid_email_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": "email", "password": "password"},
    )
    assert response.status_code == 422


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post(
        "/auth/register", json={"invalid_key": fake.email(), "password": "password"}
    )
    assert response.status_code == 422


def test_existing_user_cannot_register(test_app_with_db):
    email = fake.email()
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": email, "password": "password"},
    )

    assert response.status_code == 201
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": email, "password": "password"},
    )

    assert response.status_code == 422


def test_guest_user_can_register(test_app_with_db):
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": fake.email(), "password": "password"},
    )
    assert response.status_code == 201


def test_registered_user_can_login(test_app_with_db):
    email = fake.email()
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": email, "password": "password"},
    )
    assert response.status_code == 201

    login_response = test_app_with_db.post(
        "/auth/login",
        json={"username": email, "password": "password"},
    )
    assert login_response.status_code == 200


def test_registered_user_cannot_login_with_wrong_password(test_app_with_db):
    email = fake.email()
    response = test_app_with_db.post(
        "/auth/register",
        json={"name": fake.name(), "email": email, "password": "password"},
    )
    assert response.status_code == 201

    login_response = test_app_with_db.post(
        "/auth/login",
        json={"username": email, "password": "wrong_password"},
    )
    assert login_response.status_code == 401


def test_unregister_user_cannot_login(test_app_with_db):
    response = test_app_with_db.post(
        "/auth/login", json={"username": fake.email(), "password": "password"}
    )
    assert response.status_code == 401
    assert response.json() == {"errors": "Incorrect username or password"}
