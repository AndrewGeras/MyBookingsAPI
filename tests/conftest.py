# ruff: noqa: E402

from unittest import mock

# мокаем кэш https://github.com/long2ice/fastapi-cache/issues/49
mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda func: func
).start()


from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
from pytest import fixture
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import engine_null_pool, async_session_maker_null_pool, Base
from src.main import app
from src.utils.db_manager import DBManager
from src.utils.utils import read_file
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.examples_data import test_user_data


set_event_loop_policy(WindowsSelectorEventLoopPolicy())


@fixture(scope="session")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# фикстура для кэширования
# @fixture(scope="session", autouse=True)
# def initialize_tests_cache():
#     FastAPICache.init(backend=InMemoryBackend(), prefix="fastapi_cache")


@fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@fixture(scope="session", autouse=True)
async def setup_db(check_test_mode, db):
    hotels = read_file("tests/mock_hotels.json")
    rooms = read_file("tests/mock_rooms.json")

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await db.hotels.add_bulk([HotelAdd.model_validate(hotel) for hotel in hotels])
    await db.rooms.add_bulk([RoomAdd.model_validate(room) for room in rooms])
    await db.commit()


@fixture(scope="session", autouse=True)
async def register_test_user(setup_db, ac):
    await ac.post(url="/auth/register", json=test_user_data)


@fixture(scope="session")
async def authenticated_ac(register_test_user, ac):
    await ac.post(
        url="/auth/login",
        json=test_user_data,
    )
    yield ac
