from src.repositories.base_repo import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User


class UsersRepo(BaseRepository):
    model = UsersORM
    schema = User
