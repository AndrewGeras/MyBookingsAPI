from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
from pytest import fixture

from src.config import settings
from src.database import engine_null_pool
from src.database import Base


set_event_loop_policy(WindowsSelectorEventLoopPolicy())


@fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@fixture(scope="session", autouse=True)
async def async_main(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
