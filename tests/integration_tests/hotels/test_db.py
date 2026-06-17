from src.schemas.hotels import HotelAdd


async def test_add_hotel(check_test_mode, db):
    await db.hotels.add(
        HotelAdd(
            title="Test Hotel",
            location="Test Location"
        )
    )
    await db.commit()
