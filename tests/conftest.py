from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
from pytest import fixture
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import engine_null_pool
from src.database import Base
from src.main import app


set_event_loop_policy(WindowsSelectorEventLoopPolicy())


@fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@fixture(scope="session", autouse=True)
async def setup_db(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@fixture(scope="session", autouse=True)
async def register_test_user(setup_db):
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        await ac.post(
            url="/auth/register",
            json={
                "nickname": "TestUser",
                "email": "test@user.xyz",
                "password": "test_password",
            }
        )
