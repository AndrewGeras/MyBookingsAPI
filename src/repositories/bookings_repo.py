from datetime import date

from sqlalchemy import select
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.repositories.base_repo import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import BookingAdd
from src.repositories.mappers.mappers import BookingMapper
from src.repositories.utils import get_available_by_date


class BookingsRepo(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())

        bookings = await self.session.scalars(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in bookings.all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        cte_ = get_available_by_date(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        ).cte("available_by_date")

        available_rooms_ids = await self.session.scalars(select(cte_.c.id))

        if data.room_id in available_rooms_ids:
            return await self.add(data)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Нет доступных номеров для бронирования",
        )
