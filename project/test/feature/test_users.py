from faker import Faker

fake = Faker()


def test_get_request_returns_405(test_app_with_db):
    """endpoint does only expect a post request"""
    response = test_app_with_db.get("/users/")
    assert response.status_code == 405


def test_post_request_with_improper_body_returns_422(test_app_with_db):
    """all of email  is required"""
    response = test_app_with_db.post("/users/", json={"email": fake.email()})
    assert response.status_code == 422


def test_post_request_with_existing_information_returns_422(test_app_with_db):
    """expects users to be unique and non-existent"""
    email = fake.email()
    response = test_app_with_db.post(
        "/users/",
        json={"name": fake.name(), "email": email, "password": fake.password()},
    )
    assert response.status_code == 201

    response = test_app_with_db.post(
        "/users/",
        json={"name": fake.name(), "email": email, "password": fake.password()},
    )
    assert response.status_code == 422


def test_post_request_with_proper_body_returns_201(test_app_with_db):
    response = test_app_with_db.post(
        "/users/",
        json={"name": fake.name(), "email": fake.email(), "password": fake.password()},
    )
    assert response.status_code == 201
