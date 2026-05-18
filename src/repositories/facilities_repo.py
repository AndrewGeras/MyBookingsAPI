from src.repositories.base_repo import BaseRepository
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.schemas.facilities import Facility, RoomFacilities


class FacilitiesRepo(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomFacilityRepo(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacilities
