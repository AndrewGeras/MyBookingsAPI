from datetime import date, timedelta

async def test_book_room(db, authenticated_ac):
    response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": (await db.rooms.get_all())[0].id,
            "date_from": str(date.today()),
            "date_to": str(date.today() + timedelta(days=1))
        }
    )

    assert response.status_code == 201
    res = response.json()
    assert isinstance(res, dict)
    assert res
    assert "room_id" in res["details"]
