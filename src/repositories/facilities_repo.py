from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from src.repositories.base_repo import BaseRepository
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.schemas.facilities import Facility, RoomFacilities


class FacilitiesRepo(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomFacilityRepo(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacilities

    async def upsert_or_delete(self, room_id: int, facilities_ids: list[int]):

        facil_ids_query_result = await self.session.execute((select(self.model.facility_id)
                                                   .filter_by(room_id=room_id)))
        current_ids = set(facil_ids_query_result.scalars().all())

        deletable_ids = current_ids - set(facilities_ids)
        insertable_ids = set(facilities_ids) - current_ids

        await self.session.execute(
            (delete(self.model)
             .filter(self.model.room_id == room_id,
                     self.model.facility_id.in_(deletable_ids)))
        )

        if insertable_ids:
            await self.session.execute(
                (insert(self.model)
                 .values([{"room_id": room_id, "facility_id": facility_id}
                          for facility_id in insertable_ids])
                 .on_conflict_do_nothing(constraint="uq_room_facility")))
