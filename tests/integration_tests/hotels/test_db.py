from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_add_hotel():
    test_data = HotelAdd(title="Test Hotel",
                         location="Test Location")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        test_hotel = await db.hotels.add(test_data)
        await db.commit()
        print (f"{test_hotel=}")
