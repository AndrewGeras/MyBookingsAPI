from datetime import date
from itertools import chain

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base_repo import BaseRepository
from src.repositories.utils import get_available_by_date
from src.models.rooms import RoomsORM
from src.schemas.rooms import Rooms


class RoomsRepo(BaseRepository):
    model = RoomsORM
    schema = Rooms

    async def get_available(self,
                            hotel_id: int,
                            date_from: date,
                            date_to: date) -> [BaseModel]:
        available_rooms = get_available_by_date(date_from, date_to, hotel_id).cte()

        query = (select(self.model,
                        available_rooms.c.available_rooms)
                .options(selectinload(self.model.facilities))
                .join(available_rooms, available_rooms.c.id == self.model.id)
                .filter(self.model.id.in_(select(available_rooms.c.id)))
                )

        query_result = await self.session.execute(query)

        result_iterator = (chain(room.__dict__.items(),
                                 (("available_rooms", available_rooms),))
                           for room, available_rooms in query_result.unique())

        return [self.schema.model_validate(dict(room_data)) for room_data in result_iterator]
