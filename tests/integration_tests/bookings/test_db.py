from datetime import date, timedelta
from decimal import Decimal

from pytest import raises
from starlette.exceptions import HTTPException

from src.schemas.bookings import BookingAdd, BookingPatch


async def test_bookings_crud(db):
    test_data = {
        "user_id": (await db.users.get_all())[0].id,
        "room_id": (await db.rooms.get_all())[0].id,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=1),
        "price": Decimal("2500.00")
    }

    # test of creating
    new_booking = await db.bookings.add(
        BookingAdd(**test_data)
    )
    assert new_booking
    for key in test_data:
        assert test_data[key] == new_booking.__getattribute__(key)

    # test of reading
    booking = (await db.bookings.get_filtered(id=new_booking.id))[0]
    booking_ = await db.bookings.get_one_or_none(id=new_booking.id)
    today_checkin = await db.bookings.get_bookings_with_today_checkin()
    assert booking
    assert booking == new_booking
    assert booking_ == new_booking
    assert new_booking in today_checkin

    # test of updating
    date_to = date.today() + timedelta(days=2)
    upd_booking = await db.bookings.edit(BookingPatch(date_to=date_to), id=new_booking.id, exclude_unset=True)
    assert new_booking != upd_booking
    assert upd_booking.date_to == date_to

    # test of deleting
    await db.bookings.delete(id=new_booking.id)

    with raises(HTTPException) as exinfo:
        deleted_booking = await db.bookings.get_one_or_none(id=new_booking.id)
        assert deleted_booking is None
    assert "Информация по запросу не найдена" in str(exinfo.value)

    await db.rollback()
