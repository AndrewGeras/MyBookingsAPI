from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base_repo import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword


class UsersRepo(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        query_result = await self.session.scalars(query)
        model = query_result.one_or_none()
        if model:
            return UserWithHashedPassword.model_validate(model)

