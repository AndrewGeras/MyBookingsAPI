from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from src.repositories.base_repo import BaseRepository
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.schemas.facilities import Facility, RoomFacilities
from src.utils.handlers import ExcHandler, get_object_or_404


class FacilitiesRepo(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomFacilityRepo(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacilities

    async def upsert_or_delete(self, room_id: int, facilities: list[int] | None):
        return_ = {"deleted" : [], "inserted": []}

        if facilities is None:
            return return_

        if not facilities:
            return_.update({"deleted" : await self.delete_bulk(room_id=room_id)})

        else:
            delete_stmt = (delete(self.model)
                           .filter_by(room_id=room_id)
                           .filter(self.model.facility_id.not_in(facilities))
                           .returning(self.model))

            insert_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": facility} for facility in facilities]
            )
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(constraint="uq_room_facility").returning(self.model)

            del_result = await self.session.execute(delete_stmt)
            ins_result = await self.session.execute(do_nothing_stmt)

            return_.update({"deleted" : [self.schema.model_validate(facility)
                                         for facility in del_result.scalars().all()],
                            "inserted": [self.schema.model_validate(facility)
                                         for facility in ins_result.scalars().all()]})
        return return_
