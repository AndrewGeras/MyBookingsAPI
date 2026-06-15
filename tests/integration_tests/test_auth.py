from src.services.auth import AuthService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)

    assert payload
    assert isinstance(payload, dict)

    key = tuple(data.keys())[0]
    assert key in payload
    assert isinstance(payload[key], int)
    assert payload[key] == data[key]

    assert "exp" in payload
    assert isinstance(payload["exp"], int)

