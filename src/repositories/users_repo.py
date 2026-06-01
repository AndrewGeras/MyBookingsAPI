from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base_repo import BaseRepository
from src.models.users import UsersORM
from src.repositories.mappers.mappers import UserMapper, UserWithHashedPasswordMapper


class UsersRepo(BaseRepository):
    model = UsersORM
    mapper = UserMapper

    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        query_result = await self.session.scalars(query)
        model = query_result.one_or_none()
        if model:
            return UserWithHashedPasswordMapper.map_to_domain_entity(model)
