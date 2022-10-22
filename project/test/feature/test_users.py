import pytest
from typing import List

from faker import Faker
from pydantic import EmailStr

from app.models.user import User

fake = Faker()


@pytest.fixture
async def create_user(email: EmailStr = None, name: str = None) -> User:
    """create a user in the db"""
    email = fake.email() if email is None else email
    name = fake.name() if name is None else name

    user = User(email=email, name=name, password=fake.password())
    await user.save()

    return user


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post("/users/", json={"email": fake.email()})
    assert response.status_code == 422


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_post_request_with_existing_information_returns_422(
    test_app_with_db, anyio_backend, create_user
):
    """expects users to be unique and non-existent"""
    user = create_user

    response = test_app_with_db.post(
        "/users/",
        json={"name": fake.name(), "email": user.email, "password": fake.password()},
    )
    assert response.status_code == 422


def test_post_request_with_proper_body_returns_201(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        json={"name": fake.name(), "email": fake.email(), "password": fake.password()},
    )
    assert response.status_code == 201


def test_get_returns_all_users(test_app_with_db):
    response = test_app_with_db.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), List)


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_id_returns_user(
    test_app_with_db, anyio_backend, create_user
):
    user = create_user

    response = test_app_with_db.get("/users/{id}".format(id=user.id))
    data = response.json()

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["name"] == user.name
    assert response.status_code == 200


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
def test_delete_request_deletes_user(test_app_with_db, anyio_backend, create_user):
    user = create_user

    response = test_app_with_db.delete("/users/{id}".format(id=user.id))
    assert response.status_code == 204

    response = test_app_with_db.get("/users/{id}".format(id=user.id))
    assert response.json() == {"errors": "User Not Found"}
    assert response.status_code == 404


def test_delete_request_works_for_only_existing_users(test_app_with_db):

    response = test_app_with_db.delete("/users/0")

    assert response.json() == {"errors": "User Not Found"}
    assert response.status_code == 404


def test_update_requests_with_non_existent_user_returns_404(test_app_with_db):
    response = test_app_with_db.put("/users/0", json={"email": fake.email()})

    assert response.status_code == 404


# @pytest.mark.parametrize("anyio_backend", ["asyncio"])
# async def test_update_requests_with_existing_email_returns_422(
#     test_app_with_db, anyio_backend, create_user
# ):
#     user1 = create_user
#     user2 = create_user

#     response = test_app_with_db.put(
#         "/users/{user}".format(user=user2.id), json={"email": user1.email}
#     )

#     assert response.status_code == 422


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_update_requests_with_unique_email_returns_200(
    test_app_with_db, anyio_backend, create_user
):
    user = create_user
    email = fake.email()

    response = test_app_with_db.put(
        "/users/{user}".format(user=user.id), json={"email": email}
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/users/{id}".format(id=user.id))
    data = response.json()

    assert response.status_code == 200
    assert data["email"] != user.email
    assert data["email"] == email
    assert data["name"] == user.name
