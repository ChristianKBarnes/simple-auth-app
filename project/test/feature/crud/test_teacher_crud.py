import pytest, datetime
from app.api.crud import teacher_crud


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_with_invalid_id(test_app_with_db, anyio_backend):
    data = await teacher_crud.get(10000)

    assert data == None


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_teacher_by_invalid_teacher_code(test_app_with_db, anyio_backend):
    data = await teacher_crud.get_teacher_by_teacher_code(10000)

    assert data == None


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_teacher_by_invalid_teacher_code(test_app_with_db, anyio_backend):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = await teacher_crud.check_out(10000, date)

    assert data == 0
