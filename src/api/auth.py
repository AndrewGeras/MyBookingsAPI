from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Response, Request, Depends
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT

from src.schemas.users import UserRequestAdd, UserAdd, UserAuth
from src.database import async_session_maker
from src.repositories.users_repo import UsersRepo
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Ауторизация и аутентификация"])


@router.post("/login",
             description="<h2>Ручка для авторизации пользователя</h2>")
async def login(user_data: UserAuth,
                response: Response):
    async with async_session_maker() as session:
        user = await UsersRepo(session).get_user_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="Пользователь с таким email не найден")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token


@router.post("/register", status_code=HTTP_201_CREATED,
             description="<h2>Ручка для регистрации пользователя</h2>")
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
    hashed_password = AuthService().get_password_hash(user.password)
    new_user = UserAdd(nickname=user.nickname,
                       email=user.email,
                       hashed_password=hashed_password,
                       first_name=user.first_name,
                       last_name=user.last_name)

    async with async_session_maker() as session:
        user_data = await UsersRepo(session).add(new_user)
        await session.commit()
    return {"status": "OK", "data": user_data}


@router.get("/mпше ыефегыe",
            description="<h2>Ручка для получения данных об авторизованном пользователе</h2>")
async def auth_only(user_id: UserIdDep):
    async with async_session_maker() as session:
        user_data = await UsersRepo(session).get_one_or_none(id=user_id)
        return user_data


@router.post("/logout",
              status_code=HTTP_204_NO_CONTENT,
              description="<h2>Ручка для выхода из учётной записи</h2>")
async def logout(response: Response):
    response.delete_cookie("access_token")

