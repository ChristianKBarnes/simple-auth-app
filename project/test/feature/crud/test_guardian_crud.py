import pytest
from app.api.crud import guardian_crud


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_with_id_list(test_app_with_db, anyio_backend, create_guardian):
    guardian = create_guardian

    [data] = await guardian_crud.get([guardian.id])

    assert data["id"] == guardian.id
    assert data["last_name"] == guardian.last_name


