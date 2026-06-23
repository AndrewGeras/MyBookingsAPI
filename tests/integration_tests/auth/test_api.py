from src.utils.examples_data import test_user_data


async def test_auth_only(authenticated_ac):
    response = await authenticated_ac.get(url="/auth/me")
    assert response.status_code == 200
    user_data = response.json()
    assert isinstance(user_data, dict)
    assert user_data
    assert user_data.get("nickname") == test_user_data["nickname"]
    assert user_data.get("email") == test_user_data["email"]