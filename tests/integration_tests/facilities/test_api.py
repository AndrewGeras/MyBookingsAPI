# Перед тестированием отключи кэш и таски на ручках

facility = "wi-fi"


async def test_add_facility(ac):
    global facility
    response = await ac.post("/facilities", json={"title": facility})

    assert response.status_code == 201
    resp_data = response.json()
    assert isinstance(resp_data, dict)
    assert resp_data
    assert facility in resp_data["details"]["title"]


async def test_get_all_facilities(ac):
    global facility
    response = await ac.get("/facilities")

    assert response.status_code == 200
    resp_data = response.json()
    assert isinstance(resp_data, list)
    assert resp_data
    assert "id" and "title" in resp_data[0]
    assert resp_data[0]["title"] == facility
