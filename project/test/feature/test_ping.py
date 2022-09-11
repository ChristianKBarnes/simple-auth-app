def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {
        "environment": "testing",
        "ping": "pong!",
        "testing": True,
    }
