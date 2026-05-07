from datetime import timedelta

from pydantic import BaseModel
from sqlalchemy import select, and_, or_, between
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi.exceptions import HTTPException

from src.repositories.base_repo import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import BookingsAdd, BookingAddRequest


class BookingsRepo(BaseRepository):
    model = BookingsORM
    schema = BookingsAdd

    async def check_booked_rooms(self, book_req: BookingsAdd):
        room_id = book_req.room_id
        date_from = book_req.date_from
        date_to = book_req.date_to
        query = (select(self.model.room_id,
                       self.model.date_from,
                       self.model.date_to)
                .where(
                    and_(
                        self.model.room_id == room_id,
                        or_(
                            between(self.model.date_from, date_from, date_to - timedelta(days=1)),
                            between(self.model.date_to, date_from + timedelta(days=1), date_to)
                        )
                    )
                ))
        query_result = await self.session.execute(query)
        booked_from_to = query_result.one_or_none()
        if booked_from_to:
            return BookingAddRequest.model_validate(booked_from_to)

    async def add_booking(self, booking_data: BookingsAdd) -> BaseModel | None:
        booked_from_to = await self.check_booked_rooms(booking_data)
        if booked_from_to:
            date_from = booked_from_to.date_from
            date_to = booked_from_to.date_to
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=f"Номер уже забронирован с {date_from} по {date_to}")
        return await self.add(booking_data)
