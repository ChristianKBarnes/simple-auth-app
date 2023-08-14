import pytest
from typing import List

from faker import Faker


fake = Faker()


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post("/teachers/", json={"email": fake.email()})
    assert response.status_code == 422


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_post_request_with_existing_information_returns_422(
    test_app_with_db, anyio_backend, create_teacher
):
    """expects teachers to be unique and non-existent"""
    teacher = create_teacher

    response = test_app_with_db.post(
        "/teachers/",
        json={"name": fake.name(), "email": teacher.email, "password": fake.password()},
    )
    assert response.status_code == 422


def test_post_request_with_proper_body_returns_201(test_app_with_db):
    first_name = fake.first_name()

    response = test_app_with_db.post(
        "/teachers/",
        json={
            "first_name": first_name,
            "last_name": fake.last_name(),
            "other_names": fake.first_name(),
            "phone": fake.unique.phone_number(),
            "email": fake.unique.email()
        },
    )
    data = response.json()["teacher"]

    assert response.status_code == 201
    assert data["first_name"] == first_name


def test_get_returns_all_teachers(test_app_with_db):
    response = test_app_with_db.get("/teachers/")

    assert response.status_code == 200
    assert isinstance(response.json(), object)


def test_get_request_with_teacher_teacher_code_returns_not_found(test_app_with_db):
    response = test_app_with_db.get(
        "/teachers/?teacher_code={teacher_code}".format(
            teacher_code=fake.random_number()
        )
    )
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_id_returns_teacher(
    anyio_backend, create_teacher, test_app_with_db
):
    teacher = create_teacher

    response = test_app_with_db.get("/teachers/{id}".format(id=teacher.id))
    data = response.json()["teacher"]

    assert response.status_code == 200
    assert data["id"] == teacher.id
    assert data["first_name"] == teacher.first_name
    assert data["last_name"] == teacher.last_name
    assert str(teacher) == teacher.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_teacher_code_returns_teacher(
    test_app_with_db, anyio_backend, create_teacher
):
    teacher = create_teacher

    response = test_app_with_db.get(
        "/teachers/?teacher_code={code}".format(code=teacher.teacher_code)
    )
    
    data = response.json()["teachers"][0]

    assert response.status_code == 200
    assert data["id"] == teacher.id
    assert data["first_name"] == teacher.first_name
    assert data["last_name"] == teacher.last_name
    assert data["teacher_code"] == teacher.teacher_code
    assert str(teacher) == teacher.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
def test_delete_request_deletes_teacher(
    test_app_with_db, anyio_backend, create_teacher
):
    teacher = create_teacher

    response = test_app_with_db.delete("/teachers/{id}".format(id=teacher.id))
    assert response.status_code == 204

    response = test_app_with_db.get("/teachers/{id}".format(id=teacher.id))
    assert response.status_code == 404
    assert str(teacher) == teacher.fullname()


def test_delete_request_works_for_only_existing_teachers(test_app_with_db):
    response = test_app_with_db.delete("/teachers/0")

    assert response.json() == {"errors": "Teacher Not Found"}
    assert response.status_code == 404


def test_update_requests_with_non_existent_teacher_returns_404(test_app_with_db):
    response = test_app_with_db.put("/teachers/0", json={"last_name": fake.last_name()})

    assert response.json() == {"errors": "Teacher Not Found"}
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_update_requests_with_unique_teacher_id_returns_200(
    test_app_with_db, anyio_backend, create_teacher
):
    teacher = create_teacher
    email = fake.email()

    response = test_app_with_db.put(
        "/teachers/{teacher}".format(teacher=teacher.id), json={"email": email}
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/teachers/{id}".format(id=teacher.id))
    data = response.json()["teacher"]

    assert response.status_code == 200
    assert data["email"] != teacher.email
    assert data["email"] == email
    assert data["first_name"] == teacher.first_name
    assert str(teacher) == teacher.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_teacher_can_check_in(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 200


def test_non_existing_teacher_cannot_check_in(test_app_with_db, anyio_backend):
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=fake.random_number())
    )

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_teacher_can_check_in_more_than_once(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=teacher.teacher_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 400
    data = response.json()
    assert data["errors"] == "Teacher has already checked in"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_checked_in_teacher_can_check_out(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=teacher.teacher_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-out".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 200


def test_non_existing_teacher_cannot_check_out(test_app_with_db, anyio_backend):
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-out".format(teacher_code=fake.random_number())
    )
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_teacher_can_check_out_more_than_once(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher
    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-in".format(teacher_code=teacher.teacher_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-out".format(teacher_code=teacher.teacher_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-out".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 400
    data = response.json()
    assert data["errors"] == "Teacher has already checked out"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_teacher_cannot_check_out_if_he_has_not_checked_in(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher

    response = test_app_with_db.post(
        "teachers/{teacher_code}/check-out".format(teacher_code=teacher.teacher_code)
    )
    data = response.json()
    assert data["errors"] == "Teacher has not checked in"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_existing_teacher_qr_code_returns_200(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher

    response = test_app_with_db.get(
        "teachers/{teacher_code}/qr-code".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 200


def test_get_non_existing_teacher_qr_code_returns_404(test_app_with_db):
    response = test_app_with_db.get(
        "teachers/{teacher_code}/qr-code".format(teacher_code=fake.random_number())
    )

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_can_get_existing_teacher_attendance(
    test_app_with_db, create_teacher, anyio_backend
):
    teacher = create_teacher

    response = test_app_with_db.get(
        "teachers/{teacher_code}/attendance".format(teacher_code=teacher.teacher_code)
    )

    assert response.status_code == 200




@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_cannot_get_non_existing_teacher_attendance(
    test_app_with_db,  anyio_backend
):
    response = test_app_with_db.get(
        "teachers/{teacher_code}/attendance".format(teacher_code=fake.random_number())
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Object does not exist'}


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_can_restore_deleted_teacher(test_app_with_db, anyio_backend, create_teacher):
    teacher = create_teacher
    
    response = test_app_with_db.delete("/teachers/{id}".format(id=teacher.id))
    assert response.status_code == 204

    response = test_app_with_db.put(
        "/teachers/restore/{id}".format(id=teacher.id)
    )

    assert response.status_code == 200
    

def test_user_cannot_restore_non_existing_teacher(test_app_with_db):
    response = test_app_with_db.put(
        "/teachers/restore/0"
    )

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_welcome_teacher_with_guardians_returns_200(test_app_with_db, create_teacher, anyio_backend):
    teacher = create_teacher

    response = test_app_with_db.post("teachers/{teacher_code}/welcome".format(teacher_code=teacher.teacher_code))
    
    assert response.status_code == 200
