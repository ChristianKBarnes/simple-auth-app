import datetime, pytest
from typing import List

from faker import Faker

from app.models.guardian import Guardian

fake = Faker(["tw_GH"])


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post("/guardians/", json={"email": fake.email()})
    assert response.status_code == 422


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_post_request_with_existing_information_returns_422(
    test_app_with_db, anyio_backend, create_guardian
):
    """expects guardians to be unique and non-existent"""
    guardian = create_guardian

    response = test_app_with_db.post(
        "/guardians/",
        json={
            "name": fake.name(),
            "email": guardian.email,
            "password": fake.password(),
        },
    )
    assert response.status_code == 422
    assert str(guardian) == guardian.fullname()


def test_post_request_with_proper_body_returns_201(test_app_with_db):
    first_name = fake.first_name()

    response = test_app_with_db.post(
        "/guardians/",
        json={
            "first_name": first_name,
            "last_name": fake.last_name(),
            "other_names": fake.first_name(),
            "phone": fake.unique.phone_number(),
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data["first_name"] == first_name


def test_get_returns_all_guardians(test_app_with_db):
    response = test_app_with_db.get("/guardians/")

    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_get_request_with_guardian_phone_returns_not_found(test_app_with_db):
    response = test_app_with_db.get(
        "/guardians/?phone={phone}".format(phone=fake.phone_number())
    )
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_guardian_phone_returns_guardian(
    test_app_with_db, anyio_backend, create_guardian
):
    guardian = create_guardian

    response = test_app_with_db.get(
        "/guardians/?phone={phone}".format(phone=guardian.phone)
    )
    assert response.status_code == 200

    data = response.json()[0]
    assert data["id"] == guardian.id
    assert data["first_name"] == guardian.first_name
    assert data["last_name"] == guardian.last_name
    assert data["phone"] == guardian.phone


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_id_returns_guardian(
    test_app_with_db, anyio_backend, create_guardian
):
    guardian = create_guardian

    response = test_app_with_db.get("/guardians/{id}".format(id=guardian.id))
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == guardian.id
    assert data["first_name"] == guardian.first_name
    assert data["last_name"] == guardian.last_name
    assert str(guardian) == guardian.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
def test_delete_request_deletes_guardian(
    test_app_with_db, anyio_backend, create_guardian
):
    guardian = create_guardian

    response = test_app_with_db.delete("/guardians/{id}".format(id=guardian.id))
    assert response.status_code == 204

    response = test_app_with_db.get("/guardians/{id}".format(id=guardian.id))
    assert response.json() == {"errors": "Guardian Not Found"}
    assert response.status_code == 404
    assert str(guardian) == guardian.fullname()


def test_delete_request_works_for_only_existing_guardians(test_app_with_db):
    response = test_app_with_db.delete("/guardians/0")

    assert response.json() == {"errors": "Guardian Not Found"}
    assert response.status_code == 404


def test_update_requests_with_non_existent_guardian_returns_404(test_app_with_db):
    response = test_app_with_db.put("/guardians/0", json={"email": fake.email()})

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_update_requests_with_unique_guardian_id_returns_200(
    test_app_with_db, anyio_backend, create_guardian
):
    guardian = create_guardian
    email = fake.email()

    response = test_app_with_db.put(
        "/guardians/{guardian}".format(guardian=guardian.id), json={"email": email}
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/guardians/{id}".format(id=guardian.id))
    data = response.json()

    assert response.status_code == 200
    assert data["email"] != guardian.email
    assert data["email"] == email
    assert data["first_name"] == guardian.first_name
    assert str(guardian) == guardian.fullname()
