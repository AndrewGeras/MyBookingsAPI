from datetime import date

from pydantic import BaseModel

from src.repositories.base_repo import BaseRepository
from src.repositories.utils import get_available_by_date
from src.models.rooms import RoomsORM
from src.schemas.rooms import Rooms, AvailableRooms


class RoomsRepo(BaseRepository):
    model = RoomsORM
    schema = Rooms

    async def get_available(self,
                            hotel_id: int,
                            date_from: date,
                            date_to: date) -> [BaseModel]:
        query_result = await self.session.execute(get_available_by_date(date_from, date_to, hotel_id))

        return [AvailableRooms.model_validate(room) for room in query_result]
