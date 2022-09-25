from datetime import timedelta
import pytest

from app.utils import create_access_token


def test_create_access_token_without_data_raises_type_error():
    with pytest.raises(TypeError) as exc_info:
        create_access_token()

    assert (
        str(exc_info.value)
        == "create_access_token() missing 1 required positional argument: 'data'"
    )


def test_create_access_token_without_expires_delta_returns_access_token():
    data = {"email": "test@example.com"}
    encoded_data = create_access_token(data)

    assert isinstance(encoded_data, str)


def test_create_access_token_with_data_and_expires_delta_returns_access_token():
    data = {"email": "test@example.com"}
    encoded_data = create_access_token(data, timedelta(minutes=2))

    assert isinstance(encoded_data, str)
