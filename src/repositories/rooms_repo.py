from src.repositories.base_repo import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Rooms


class RoomsRepo(BaseRepository):
    model = RoomsORM
    schema = Rooms
