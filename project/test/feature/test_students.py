import pytest
from typing import List

from faker import Faker


fake = Faker()


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post("/students/", json={"email": fake.email()})
    assert response.status_code == 422


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_post_request_with_existing_information_returns_422(
    test_app_with_db, anyio_backend, create_student
):
    """expects students to be unique and non-existent"""
    student = create_student

    response = test_app_with_db.post(
        "/students/",
        json={"name": fake.name(), "email": student.email, "password": fake.password()},
    )
    assert response.status_code == 422


def test_post_request_with_proper_body_returns_201(test_app_with_db):
    first_name = fake.first_name()

    response = test_app_with_db.post(
        "/students/",
        json={
            "first_name": first_name,
            "last_name": fake.last_name(),
            "other_names": fake.first_name(),
        },
    )
    data = response.json()["student"]

    assert response.status_code == 201
    assert data["first_name"] == first_name


def test_get_returns_all_students(test_app_with_db):
    response = test_app_with_db.get("/students/")

    assert response.status_code == 200
    assert isinstance(response.json(), object)


def test_get_request_with_student_student_code_returns_not_found(test_app_with_db):
    response = test_app_with_db.get(
        "/students/?student_code={student_code}".format(
            student_code=fake.random_number()
        )
    )
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_post_request_with_guardians_creates_student_guardian_relation(
    test_app_with_db, anyio_backend, create_guardian
):
    first_name = fake.first_name()
    guardian = create_guardian

    response = test_app_with_db.post(
        "/students/",
        json={
            "first_name": first_name,
            "last_name": fake.last_name(),
            "other_names": fake.first_name() if fake.boolean else None,
            "guardians": [guardian.id],
        },
    )
    data = response.json()["student"]

    assert response.status_code == 201
    assert data["first_name"] == first_name


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_put_request_with_guardians_creates_student_guardian_relation(
    test_app_with_db, anyio_backend, create_guardian, create_student
):
    student = create_student
    guardian = create_guardian

    response = test_app_with_db.put(
        "/students/{id}".format(id=student.id),
        json={
            "guardians": [guardian.id],
        },
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/students/{0}/guardians".format(student.student_code))
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data['guardians'], List)
    for g in data['guardians']:
        assert g["id"] == guardian.id



@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_put_request_with_invalid_guardians_does_not_creates_student_guardian_relation(
    test_app_with_db, anyio_backend, create_student
):
    first_name = fake.first_name()
    student = create_student

    response = test_app_with_db.put(
        "/students/{id}".format(id=student.id),
        json={
            "first_name": first_name,
            "guardians": [4000],
        },
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/students/{0}/guardians".format(student.student_code))
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data['guardians'], List)
    for guardian in data['guardians']:
        assert guardian.id != 4000


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_id_returns_student(
    anyio_backend, create_student, test_app_with_db
):
    student = create_student

    response = test_app_with_db.get("/students/{id}".format(id=student.id))
    data = response.json()["student"]

    assert response.status_code == 200
    assert data["id"] == student.id
    assert data["first_name"] == student.first_name
    assert data["last_name"] == student.last_name
    assert str(student) == student.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_request_with_student_code_returns_student(
    test_app_with_db, anyio_backend, create_student
):
    student = create_student

    response = test_app_with_db.get(
        "/students/?student_code={code}".format(code=student.student_code)
    )
    data = response.json()["students"][0]

    assert response.status_code == 200
    assert data["id"] == student.id
    assert data["first_name"] == student.first_name
    assert data["last_name"] == student.last_name
    assert data["student_code"] == student.student_code
    assert str(student) == student.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
def test_delete_request_deletes_student(
    test_app_with_db, anyio_backend, create_student
):
    student = create_student

    response = test_app_with_db.delete("/students/{id}".format(id=student.id))
    assert response.status_code == 204

    response = test_app_with_db.get("/students/{id}".format(id=student.id))
    assert response.status_code == 404
    assert str(student) == student.fullname()


def test_delete_request_works_for_only_existing_students(test_app_with_db):
    response = test_app_with_db.delete("/students/0")

    assert response.json() == {"errors": "Student Not Found"}
    assert response.status_code == 404


def test_update_requests_with_non_existent_student_returns_404(test_app_with_db):
    response = test_app_with_db.put("/students/0", json={"email": fake.email()})

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_update_requests_with_unique_student_id_returns_200(
    test_app_with_db, anyio_backend, create_student
):
    student = create_student
    email = fake.email()

    response = test_app_with_db.put(
        "/students/{student}".format(student=student.id), json={"email": email}
    )
    assert response.status_code == 200

    response = test_app_with_db.get("/students/{id}".format(id=student.id))
    data = response.json()["student"]

    assert response.status_code == 200
    assert data["email"] != student.email
    assert data["email"] == email
    assert data["first_name"] == student.first_name
    assert str(student) == student.fullname()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_student_can_check_in(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )

    assert response.status_code == 200


def test_non_existing_student_cannot_check_in(test_app_with_db, anyio_backend):
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=fake.random_number())
    )

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_student_can_check_in_more_than_once(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )

    assert response.status_code == 400
    data = response.json()
    assert data["errors"] == "Student has already checked in"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_checked_in_student_can_check_out(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=student.student_code)
    )

    assert response.status_code == 200


def test_non_existing_student_cannot_check_out(test_app_with_db, anyio_backend):
    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=fake.random_number())
    )
    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_student_can_check_out_more_than_once(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=student.student_code)
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=student.student_code)
    )

    assert response.status_code == 400
    data = response.json()
    assert data["errors"] == "Student has already checked out"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_existing_student_cannot_check_out_if_he_has_not_checked_in(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student

    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=student.student_code)
    )
    data = response.json()
    assert data["errors"] == "Student has not checked in"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_existing_student_qr_code_returns_200(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student

    response = test_app_with_db.get(
        "students/{student_code}/qr-code".format(student_code=student.student_code)
    )

    assert response.status_code == 200


def test_get_non_existing_student_qr_code_returns_404(test_app_with_db):
    response = test_app_with_db.get(
        "students/{student_code}/qr-code".format(student_code=fake.random_number())
    )

    assert response.status_code == 404


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_can_get_existing_student_attendance(
    test_app_with_db, create_student, anyio_backend
):
    student = create_student

    response = test_app_with_db.get(
        "students/{student_code}/attendance".format(student_code=student.student_code)
    )

    assert response.status_code == 200




@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_cannot_get_non_existing_student_attendance(
    test_app_with_db,  anyio_backend
):
    response = test_app_with_db.get(
        "students/{student_code}/attendance".format(student_code=fake.random_number())
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Object does not exist'}


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_student_with_guardian_receives_email_when_checked_in(
    test_app_with_db,  anyio_backend, create_student, create_guardian
):
    first_name = fake.first_name()
    student = create_student
    guardian = create_guardian

    response = test_app_with_db.put(
        "/students/{id}".format(id=student.id),
        json={
            "first_name": first_name,
            "guardians": [guardian.id],
        },
    )
    assert response.status_code == 200

    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )
    



@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_student_with_guardian_receives_email_when_checked_out(
    test_app_with_db,  anyio_backend, create_student, create_guardian
):
    first_name = fake.first_name()
    student = create_student
    guardian = create_guardian

    response = test_app_with_db.put(
        "/students/{id}".format(id=student.id),
        json={
            "first_name": first_name,
            "guardians": [guardian.id],
        },
    )
    assert response.status_code == 200
    
    response = test_app_with_db.post(
        "students/{student_code}/check-in".format(student_code=student.student_code)
    )

    response = test_app_with_db.post(
        "students/{student_code}/check-out".format(student_code=student.student_code)
    )


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_user_can_restore_deleted_student(test_app_with_db, anyio_backend, create_student):
    student = create_student
    
    response = test_app_with_db.delete("/students/{id}".format(id=student.id))
    assert response.status_code == 204

    response = test_app_with_db.put(
        "/students/restore/{id}".format(id=student.id)
    )

    assert response.status_code == 200
    

def test_user_cannot_restore_non_existing_student(test_app_with_db):
    response = test_app_with_db.put(
        "/students/restore/0"
    )

    assert response.status_code == 404
    

@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_welcome_student_with_guardians_returns_200(test_app_with_db, create_student, create_guardian, anyio_backend):
    student = create_student
    test_app_with_db.put(
        "/students/{id}".format(id=student.id),
        json={
            "guardians": [create_guardian.id],
        },
    )

    response = test_app_with_db.post("students/{student_code}/welcome".format(student_code=student.student_code))
    
    assert response.status_code == 200


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_welcome_student_without_guardians_returns_200(test_app_with_db, create_student, anyio_backend):
    response = test_app_with_db.post("students/{student_code}/welcome".format(student_code=create_student.student_code))
    
    assert response.status_code == 200
