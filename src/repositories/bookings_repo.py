from datetime import date

from sqlalchemy import select

from src.repositories.base_repo import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingMapper


class BookingsRepo(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_bookings_with_today_checkin(self):
        query = (select(self.model)
                 .filter(self.model.date_from==date.today()))

        bookings = await self.session.scalars(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in bookings.all()]
