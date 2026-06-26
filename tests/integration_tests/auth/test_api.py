import pytest

from src.utils.examples_data import test_auth_data


@pytest.fixture(scope="session")
async def clear_users(db):
    await db.users.clear_all()
    await db.commit()


@pytest.mark.parametrize(
    "nickname, email, password, first_name, last_name, auth_status, login, pass_code, login_status, logged_status",
    test_auth_data,
)
async def test_auth_flow(
    nickname: str,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    auth_status: int,
    login: str,
    pass_code: str,
    login_status: int,
    logged_status: int,
    ac,
    db,
    clear_users,
):
    register_resp = await ac.post(
        url="/auth/register",
        json={
            "nickname": nickname,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    auth_user = register_resp.json()
    AUTH_SC = register_resp.status_code
    assert AUTH_SC == auth_status
    if AUTH_SC == 201:
        assert auth_user["details"]["nickname"] == nickname
        assert auth_user["details"]["email"] == email
        assert auth_user["details"]["first_name"] == first_name
        assert auth_user["details"]["last_name"] == last_name
        assert "access_token" not in ac.cookies

    login_resp = await ac.post(
        url="/auth/login", json={"email": login, "password": pass_code}
    )

    LOGIN_SC = login_resp.status_code
    assert LOGIN_SC == login_status
    if LOGIN_SC == 200:
        assert "access_token" in ac.cookies

    auth_only_resp = await ac.get(url="/auth/me")
    auth_only_user = auth_only_resp.json()
    AUTH_ONLY_SC = auth_only_resp.status_code
    assert AUTH_ONLY_SC == logged_status
    if AUTH_ONLY_SC == 200:
        assert "access_token" in ac.cookies
        assert "password" not in auth_only_user
        assert "hashed_password" not in auth_only_user
        assert auth_only_user["email"] == login

    logout_resp = await ac.post(url="/auth/logout")
    assert logout_resp.status_code == 204
    assert "access_token" not in ac.cookies
