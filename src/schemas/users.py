from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    nickname: str   # добавить валидацию на непустую строку
    email: EmailStr
    password: str   # добавить валидацию на непустую строку
    first_name: str | None = None
    last_name: str | None = None


class UserAdd(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserWithHashedPassword(User):
    hashed_password: str
