from src.repositories.base_repo import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingMapper


class BookingsRepo(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper
