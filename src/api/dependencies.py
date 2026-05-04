from typing import Annotated

from fastapi import Depends, Query, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED

from jwt.exceptions import PyJWTError

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page:  Annotated[int, Query(1, description="номер страницы", gt=0),]
    per_page: Annotated[int | None, Query(None, description="количество отелей на странице", gt=0, le=30)]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")
    return access_token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        payload = AuthService().decode_token(token)
        return payload.get("user_id")
    except PyJWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Токена доступа недействителен")

UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]