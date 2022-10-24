import pytest, datetime
from app.api.crud import student_crud


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_with_invalid_id(test_app_with_db, anyio_backend):
    data = await student_crud.get(10000)

    assert data == None


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_student_by_invalid_student_code(test_app_with_db, anyio_backend):
    data = await student_crud.get_student_by_student_code(10000)

    assert data == None


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_student_by_invalid_student_code(test_app_with_db, anyio_backend):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    data = await student_crud.check_out(10000, date)

    assert data == 0
