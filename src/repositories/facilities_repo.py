from src.repositories.base_repo import BaseRepository
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import Facility


class FacilitiesRepo(BaseRepository):
    model = FacilitiesORM
    schema = Facility