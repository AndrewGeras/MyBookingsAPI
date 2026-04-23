from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserAdd(BaseModel):
    nickname: str
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str