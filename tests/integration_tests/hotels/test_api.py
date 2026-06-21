async def test_get_hotels(ac):
    response = await ac.get("/hotels",
                            # по умолчанию будут подтягиваться текущая и следующая даты (default значения из ручки),
                            # но при желании можно задать свои через словарь params:
                            # params={"date_from": "2026-06-19",
                            #         "date_to": "2026-06-20"}
                            )
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data
    assert isinstance(resp_data, list)

    assert "id" in resp_data[0]
    assert "title" in resp_data[0]
    assert "location" in resp_data[0]