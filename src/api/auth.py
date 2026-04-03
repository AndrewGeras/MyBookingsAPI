from typing import Annotated
from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED
from pwdlib import PasswordHash

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users_repo import UsersRepo


router = APIRouter(prefix="/register", tags=["Ауторизация и аутентификация"])

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)


@router.post("/", status_code=HTTP_201_CREATED)
async def register_user(user: Annotated[UserRequestAdd, Body(openapi_examples={
                        "valid": {
                                "summary": "Валидные данные",
                                "description": "Пример **валидных** данных пользователя.",
                                "value": {"nickname": "VasPup",
                                          "email": "vpupkin@qwerty.bzd",
                                          "password": "pupkin123",
                                          "first_name": "Василий",
                                          "last_name": "Пупкин"
                                          }
                            }
                        })
                    ]):
    hashed_password = get_password_hash(user.password)
    new_user = UserAdd(nickname=user.nickname,
                       email=user.email,
                       hashed_password=hashed_password,
                       first_name=user.first_name,
                       last_name=user.last_name)

    async with async_session_maker() as session:
        user_data = await UsersRepo(session).add(new_user)
        await session.commit()
    return {"status": "OK", "data": user_data}