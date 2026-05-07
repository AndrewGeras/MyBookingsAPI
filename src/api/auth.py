from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.schemas.users import UserRequestAdd, UserAdd, UserAuth
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.utils.examples_data import user_example

router = APIRouter(prefix="/auth", tags=["Ауторизация и аутентификация"])


@router.post("/register", status_code=HTTP_201_CREATED,
             description="<h2>Ручка для регистрации пользователя</h2>")
async def register_user(db: DBDep, user: Annotated[UserRequestAdd, Body(openapi_examples=user_example)]):
    hashed_password = AuthService().get_password_hash(user.password)
    new_user = UserAdd(nickname=user.nickname,
                       email=user.email,
                       hashed_password=hashed_password,
                       first_name=user.first_name,
                       last_name=user.last_name)

    user_data = await db.users.add(new_user)
    await db.commit()
    return {"status": "success", "message": "Пользователь зарегистрирован", "details": user_data}


@router.post("/login",
             description="<h2>Ручка для авторизации пользователя</h2>")
async def login(db: DBDep, user_data: UserAuth,
                response: Response):
    user = await db.users.get_user_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Пользователь с таким email не найден")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Неверный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"message": "доступ разрешён", "user_data": user_data}


@router.get("/mе",
            description="<h2>Ручка для получения данных об авторизованном пользователе</h2>")
async def auth_only(db: DBDep, user_id: UserIdDep):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout",
              status_code=HTTP_204_NO_CONTENT,
              description="<h2>Ручка для выхода из учётной записи</h2>")
async def logout(response: Response):
    response.delete_cookie("access_token")
