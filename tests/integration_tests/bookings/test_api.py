from datetime import date, timedelta

import pytest

room_id_ = 1
today_ = str(date.today())
tomorrow_ = str(date.today() + timedelta(days=1))


@pytest.fixture(scope="session")
async def clear_bookings(db):
    await db.bookings.clear_all()
    await db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (room_id_, today_, tomorrow_, 201),
    (room_id_, today_, tomorrow_, 201),
    (room_id_, today_, tomorrow_, 201),
    (room_id_, today_, tomorrow_, 201),
    (room_id_, today_, tomorrow_, 201),
    (room_id_, today_, tomorrow_, 400),
])
async def test_book_room(db, authenticated_ac, room_id, date_from, date_to, status_code):
    response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    res_status_code = response.status_code
    assert res_status_code == status_code
    res = response.json()
    assert isinstance(res, dict)
    assert res
    if res_status_code == 200:
        assert "room_id" in res["details"]
    if res_status_code == 400:
        assert res["detail"] == "Нет доступных номеров для бронирования"


@pytest.mark.parametrize("room_id, date_from, date_to, post_status, get_status, bookings_num", [
    (room_id_, today_, tomorrow_, 201, 200, 1),
    (room_id_, today_, tomorrow_, 201, 200, 2),
    (room_id_, today_, tomorrow_, 201, 200, 3),
    (room_id_, today_, tomorrow_, 201, 200, 4),
    (room_id_, today_, tomorrow_, 201, 200, 5),
    (room_id_, today_, tomorrow_, 400, 200, 5),
])
async def test_add_and_get_bookings(authenticated_ac,
                                    clear_bookings,
                                    room_id,
                                    date_from,
                                    date_to,
                                    post_status,
                                    get_status,
                                    bookings_num):
    add_booking_res = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    my_bookings_res = await authenticated_ac.get(url="/bookings/me")

    add_booking_res_status_code = add_booking_res.status_code
    my_bookings_res_status_code = my_bookings_res.status_code
    res = my_bookings_res.json()

    assert add_booking_res_status_code == post_status
    assert my_bookings_res_status_code == get_status
    assert isinstance(res, list)
    assert len(res) == bookings_num
